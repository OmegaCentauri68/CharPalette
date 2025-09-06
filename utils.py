"""
Utility functions for CharPalette application.
"""

from PySide6.QtWidgets import QApplication
import regex
import json
import os


class FileUtils:
    """Utility class for file operations."""

    @staticmethod
    def load_config(config_path: str = 'config/tabs.json') -> dict:
        """
        Load configuration from JSON file.

        Args:
            config_path: Path to the config file

        Returns:
            Dictionary containing configuration data
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f'Error loading config: {e}')
            return {'tabs': []}

    @staticmethod
    def load_symbols_from_file(filename: str, symbol_type: str = 'emoji') -> list[str]:
        """
        Load symbols from a txt file.

        Args:
            filename: Path to the symbol file
            symbol_type: Type of symbols ('emoji' or 'symbol')

        Returns:
            List of symbol strings
        """
        if not os.path.exists(filename):
            print(f'File not found: {filename}')
            return []

        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.read().strip().split('\n')

                if symbol_type == 'emoji':
                    # For emoji files, each line should contain one emoji (which can be multi-codepoint)
                    symbols = [line.strip() for line in lines if line.strip()]
                else:
                    # For symbol files, each line contains one symbol
                    symbols = [line.strip() for line in lines if line.strip()]

                return symbols
        except Exception as e:
            print(f'Error loading symbols from {filename}: {e}')
            return []

    @staticmethod
    def load_emojis_from_file(filename: str) -> list[str]:
        """
        Legacy method for backward compatibility.
        Load emojis from a txt file.

        Args:
            filename: Path to the emoji file

        Returns:
            List of emoji strings
        """
        return FileUtils.load_symbols_from_file(filename, 'emoji')


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
