"""Entry point for text-to-telegram."""

import argparse
import asyncio
from pathlib import Path

from telegram.ext import Application, MessageHandler as TelegramMessageHandler, filters

from .config import load_config
from .bot import MessageHandler
from .watcher import InputWatcher


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Telegram bot that bridges messages to/from text files"
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to config file (default: ./config.json)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=500,
        help="Poll interval in milliseconds (default: 500)",
    )
    return parser.parse_args()


async def run_watcher(watcher: InputWatcher) -> None:
    """Run the input watcher as a background task."""
    await watcher.run()


def main() -> None:
    args = parse_args()

    # Load config
    config_path = args.config or Path("config.json")
    config = load_config(config_path)

    # Set up the application
    app = Application.builder().token(config.token).build()

    # Set up message handler
    handler = MessageHandler(config.chat_id)
    app.add_handler(
        TelegramMessageHandler(filters.TEXT & ~filters.COMMAND, handler.handle_message)
    )

    # Set up input watcher
    watcher = InputWatcher(app.bot, config.chat_id, args.interval)

    # Run both the bot and the watcher
    async def run_all() -> None:
        async with app:
            await app.start()
            await app.updater.start_polling()
            print(f"Bot started. Watching for messages in chat {config.chat_id}")
            print(f"Write to input.txt to send messages, read content.txt for incoming")

            # Run watcher in the foreground
            try:
                await watcher.run()
            except asyncio.CancelledError:
                pass
            finally:
                await app.updater.stop()
                await app.stop()

    try:
        asyncio.run(run_all())
    except KeyboardInterrupt:
        print("\nShutting down...")


if __name__ == "__main__":
    main()
