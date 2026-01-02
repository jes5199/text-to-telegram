"""Input file watcher - monitors input.txt and sends messages."""

import asyncio
import tempfile
from pathlib import Path

from telegram import Bot
from telegram.error import TelegramError


class InputWatcher:
    def __init__(self, bot: Bot, chat_id: int, interval_ms: int = 500):
        self.bot = bot
        self.chat_id = chat_id
        self.interval = interval_ms / 1000
        self.input_path = Path("input.txt")

    async def run(self) -> None:
        """Watch input.txt and send messages."""
        while True:
            await self._process_input()
            await asyncio.sleep(self.interval)

    async def _process_input(self) -> None:
        """Process one line from input.txt if available."""
        if not self.input_path.exists():
            return

        try:
            content = self.input_path.read_text()
        except OSError:
            return

        if not content:
            return

        # Find first complete line
        newline_pos = content.find("\n")
        if newline_pos == -1:
            return  # No complete line yet

        line = content[:newline_pos]
        remaining = content[newline_pos + 1:]

        if not line:
            # Empty line, just remove it
            self._atomic_write(remaining)
            return

        # Process escape sequences
        message = line.replace("\\n", "\n")

        # Skip empty or whitespace-only messages
        if not message.strip():
            self._atomic_write(remaining)
            return

        # Try to send
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=message)
        except TelegramError as e:
            print(f"Failed to send message: {e}")
            # Remove the line anyway to avoid infinite retry
            self._atomic_write(remaining)
            return

        # Success - remove the line
        self._atomic_write(remaining)

    def _atomic_write(self, content: str) -> None:
        """Atomically write content to input.txt."""
        # Write to temp file, then rename
        fd, tmp_path = tempfile.mkstemp(dir=self.input_path.parent)
        try:
            with open(fd, "w") as f:
                f.write(content)
            Path(tmp_path).rename(self.input_path)
        except OSError:
            try:
                Path(tmp_path).unlink()
            except OSError:
                pass
