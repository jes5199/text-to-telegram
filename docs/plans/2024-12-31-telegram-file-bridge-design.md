# Telegram File Bridge Design

A Telegram bot that bridges messages to/from text files, following the file-tmux-file pattern.

## Overview

Single long-running daemon with two concurrent tasks:
1. **Telegram listener** - Receives messages, appends to `content.txt`
2. **Input watcher** - Monitors `input.txt`, sends complete lines to Telegram

## File Interface

Files are created in the current working directory:

- `content.txt` - Incoming messages (append-only log)
- `input.txt` - Outgoing queue (consumed line-by-line)

### content.txt format

```
[2024-12-31 22:15:03] Hello there
[2024-12-31 22:16:47] What's the status?
```

Timestamp + message, one per line. External process may trim from the top.

### input.txt format

```
First message
Line one\nLine two\nLine three
Another message
```

Each line ending with `\n` is sent as a message, then removed. Literal `\n` in the line creates multi-line messages.

## Configuration

Config file with bot token and chat ID:

```json
{
  "token": "123456:ABC-...",
  "chat_id": 123456789
}
```

Location: CLI argument `--config`, falls back to `./config.json`.

## CLI Interface

```bash
# Basic usage
text-to-telegram

# Custom config
text-to-telegram --config /path/to/config.json

# Custom poll interval (default 500ms)
text-to-telegram --interval 250
```

## Project Structure

```
text-to-telegram/
├── src/
│   └── text_to_telegram/
│       ├── __init__.py
│       ├── __main__.py   # Entry point, CLI parsing
│       ├── bot.py        # Telegram handler
│       ├── watcher.py    # Input file watcher
│       └── config.py     # Config loading
├── config.json
└── pyproject.toml
```

## Concurrency

Using python-telegram-bot's async architecture:
- Telegram polling handled by library
- File watcher as async loop checking every N ms
- Atomic file operations (temp file + rename) for input.txt

## Error Handling

**Sending errors:**
- Network issues: retry with backoff
- Invalid message: log error, remove line
- Rate limiting: respect limits, queue backs up

**File errors:**
- input.txt missing: nothing to send (normal)
- content.txt write fail: log, retry next poll
- Permission errors: fatal exit

**Startup:**
- Missing/invalid config: exit with clear message
- Auth failure: exit with error

## Dependencies

- python-telegram-bot
