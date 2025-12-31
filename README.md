# text-to-telegram

A Telegram bot that bridges messages to/from text files, following the [file-tmux-file](https://github.com/...) pattern.

## What It Does

- **Receives** Telegram messages and appends them to `content.txt`
- **Sends** lines from `input.txt` to Telegram, removing them after delivery

This enables programmatic interaction with Telegram through simple file operations.

## Installation

Requires Python 3.10+ and a Telegram bot token.

```bash
# Using uv (recommended)
uv pip install -e .

# Or using pip
pip install -e .
```

## Setup

1. Create a bot via [@BotFather](https://t.me/botfather) and get the token
2. Start a chat with your bot and send any message
3. Get your chat ID by visiting:
   ```
   https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   ```
   Look for `"chat":{"id":123456789}` in the response.

4. Create `config.json`:
   ```json
   {
     "token": "123456:ABC-your-bot-token",
     "chat_id": 123456789
   }
   ```

## Usage

```bash
# Run from the directory where you want files created
text-to-telegram

# Custom config file location
text-to-telegram --config /path/to/config.json

# Custom poll interval (default 500ms)
text-to-telegram --interval 250
```

### CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `--config PATH` | `./config.json` | Path to config file |
| `--interval MS` | `500` | Poll interval in milliseconds |

## File Interface

The bot creates/uses files in the current working directory:

### content.txt

Incoming messages are appended with timestamps:

```
[2024-12-31 22:15:03] Hello there
[2024-12-31 22:16:47] What's the status?
```

Multi-line messages have newlines escaped as `\n`.

### input.txt

Write lines here to send them to Telegram:

```
First message
Second message
```

Each complete line (ending with newline) is sent and removed. The file remains empty after all messages are sent.

For multi-line messages, use literal `\n`:

```
Line one\nLine two\nLine three
```

This sends as:
```
Line one
Line two
Line three
```

## Configuration

### config.json

```json
{
  "token": "123456:ABC-your-bot-token",
  "chat_id": 123456789
}
```

| Field | Description |
|-------|-------------|
| `token` | Bot token from @BotFather |
| `chat_id` | Numeric ID of the chat to bridge |

## Dependencies

- [python-telegram-bot](https://python-telegram-bot.org/)

## License

MIT
