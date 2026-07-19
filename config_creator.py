import configparser
from getpass import getpass


def main() -> None:
    api_id = input("Telegram API ID: ").strip()
    api_hash = getpass("Telegram API hash: ").strip()
    session_name = input("Local session name [telegram_exporter]: ").strip()
    session_name = session_name or "telegram_exporter"

    config = configparser.ConfigParser()
    config["Telegram"] = {
        "api_id": api_id,
        "api_hash": api_hash,
        "session_name": session_name,
    }

    with open("config.ini", "w", encoding="utf-8") as config_file:
        config.write(config_file)

    print("Created config.ini. Keep it private; it is excluded by .gitignore.")


if __name__ == "__main__":
    main()
