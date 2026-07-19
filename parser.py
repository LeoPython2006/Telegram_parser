import argparse
import configparser
import json
from datetime import datetime

from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import ChannelParticipantsSearch


class DateTimeEncoder(json.JSONEncoder):
    def default(self, value):
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, bytes):
            return list(value)
        return super().default(value)


def load_config(path: str = "config.ini") -> tuple[int, str, str]:
    config = configparser.ConfigParser()
    if not config.read(path):
        raise FileNotFoundError(
            f"{path} was not found. Copy config.example.ini to config.ini first."
        )

    telegram = config["Telegram"]
    return (
        telegram.getint("api_id"),
        telegram["api_hash"],
        telegram.get("session_name", "telegram_exporter"),
    )


async def dump_participants(client, channel) -> None:
    offset = 0
    limit = 100
    participants = []
    participant_filter = ChannelParticipantsSearch("")

    while True:
        batch = await client(
            GetParticipantsRequest(
                channel=channel,
                filter=participant_filter,
                offset=offset,
                limit=limit,
                hash=0,
            )
        )
        if not batch.users:
            break
        participants.extend(batch.users)
        offset += len(batch.users)

    payload = [
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "phone": user.phone,
            "is_bot": user.bot,
        }
        for user in participants
    ]

    with open("channel_users.json", "w", encoding="utf-8") as output:
        json.dump(payload, output, ensure_ascii=False, indent=2)


async def dump_messages(client, channel) -> None:
    offset_id = 0
    messages = []

    while True:
        history = await client(
            GetHistoryRequest(
                peer=channel,
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                limit=100,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
        if not history.messages:
            break

        messages.extend(message.to_dict() for message in history.messages)
        offset_id = history.messages[-1].id

    with open("channel_messages.json", "w", encoding="utf-8") as output:
        json.dump(
            messages,
            output,
            ensure_ascii=False,
            indent=2,
            cls=DateTimeEncoder,
        )


async def export_channel(client, channel_reference: str) -> None:
    channel = await client.get_entity(channel_reference)
    await dump_participants(client, channel)
    await dump_messages(client, channel)
    print("Export completed: channel_users.json and channel_messages.json")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export Telegram channel participants and messages to JSON."
    )
    parser.add_argument(
        "--channel",
        required=True,
        help="Telegram channel username, invite link, or URL.",
    )
    parser.add_argument(
        "--config",
        default="config.ini",
        help="Path to the local credentials file.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    api_id, api_hash, session_name = load_config(args.config)
    client = TelegramClient(session_name, api_id, api_hash)

    with client:
        client.loop.run_until_complete(export_channel(client, args.channel))
