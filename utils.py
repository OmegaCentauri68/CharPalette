"""
Utility functions for CharPalette application.
"""

from PySide6.QtWidgets import QApplication
import regex


class FileUtils:
    """Utility class for file operations."""

    @staticmethod
    def load_emojis_from_file(filename: str) -> list[str]:
        """
        Load emojis from a txt file.

        Args:
            filename: Path to the emoji file

        Returns:
            List of emoji strings
        """
        with open(filename, 'r', encoding='utf-8') as file:
            content: str = file.read()
            # Use regex to match emoji sequences and filter out whitespace
            emojis: list[str] = [
                match.group()
                for match in regex.finditer(r'\X', content)
                if not match.group().isspace()
            ]
            return emojis


class ClipboardUtils:
    """Utility class for clipboard operations."""

    @staticmethod
    def copy_to_clipboard(text: str) -> None:
        """
        Copy text to system clipboard.

        Args:
            text: Text to copy to clipboard
        """
        clipboard = QApplication.instance().clipboard()
        clipboard.setText(text)
