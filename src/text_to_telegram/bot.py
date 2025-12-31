"""Telegram message handler - receives messages and writes to content.txt."""

from datetime import datetime
from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes


class MessageHandler:
    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.content_path = Path("content.txt")

    async def handle_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle incoming message - append to content.txt."""
        if update.message is None:
            return

        # Only process messages from the configured chat
        if update.message.chat_id != self.chat_id:
            return

        text = update.message.text
        if text is None:
            return

        # Format: [YYYY-MM-DD HH:MM:SS] message
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Escape newlines in the message for single-line log format
        escaped_text = text.replace("\n", "\\n")
        line = f"[{timestamp}] {escaped_text}\n"

        # Append to content.txt
        try:
            with open(self.content_path, "a") as f:
                f.write(line)
        except OSError as e:
            print(f"Failed to write to content.txt: {e}")
