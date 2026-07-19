<div align="center">

# Telegram Channel Exporter

### Export channel participants and message history to structured JSON

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Telethon](https://img.shields.io/badge/Telethon-MTProto-2CA5E0?style=flat-square)
![Output](https://img.shields.io/badge/output-JSON-111827?style=flat-square)

</div>

## Overview

A small Telethon utility that exports accessible Telegram channel data into two files:

- **channel_users.json** — participant metadata
- **channel_messages.json** — message history with JSON-safe dates and byte values

Use this tool only for channels you own or are authorized to process, and follow Telegram policies and applicable privacy law.

## Setup

~~~bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp config.example.ini config.ini
~~~

Create Telegram API credentials at [my.telegram.org](https://my.telegram.org), then add them to **config.ini**. The file is ignored by Git.

## Usage

~~~bash
python parser.py --channel "https://t.me/example_channel"
~~~

On first run, Telethon may request a login code and create a local session file. Session files grant account access and must never be committed or shared.

## How it works

~~~mermaid
flowchart LR
    A[Telegram channel] --> B[Telethon client]
    B --> C[Participant pagination]
    B --> D[Message pagination]
    C --> E[channel_users.json]
    D --> F[channel_messages.json]
~~~

## Security

- Credentials and session files are excluded through **.gitignore**.
- Rotate any API credentials that were previously committed.
- Revoke exposed Telegram sessions from **Settings → Devices**.
- Avoid exporting personal data without a lawful basis and user consent.

## Limitations

Telegram permissions, privacy settings, rate limits, and channel size can affect export completeness.
