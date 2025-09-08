#!/usr/bin/env python3
"""
Test script to verify Noto Color Emoji font loading
"""

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
import sys
import os

def test_font_loading():
    """Test if Noto Color Emoji font loads successfully."""
    app = QApplication(sys.argv)

    font_db = QFontDatabase()
    fonts_dir = os.path.join('assets', 'fonts')

    print("Available system fonts (emoji-related):")
    for family in font_db.families():
        if any(keyword in family.lower() for keyword in ['emoji', 'color', 'noto']):
            print(f"  - {family}")

    print(f"\nLooking for fonts in: {fonts_dir}")

    if os.path.exists(fonts_dir):
        for font_file in os.listdir(fonts_dir):
            if font_file.endswith(('.ttf', '.otf')):
                font_path = os.path.join(fonts_dir, font_file)
                print(f"\nLoading font: {font_path}")
                font_id = font_db.addApplicationFont(font_path)
                if font_id != -1:
                    font_families = font_db.applicationFontFamilies(font_id)
                    print(f"✅ Successfully loaded font families: {font_families}")

                    # Check if Noto Color Emoji is available
                    for family in font_families:
                        if 'Noto' in family and 'Emoji' in family:
                            print(f"🎉 Found Noto Color Emoji: {family}")
                else:
                    print(f"❌ Failed to load font: {font_path}")
    else:
        print(f"❌ Fonts directory not found: {fonts_dir}")

    print(f"\nAll available fonts after loading:")
    all_families = font_db.families()
    emoji_fonts = [f for f in all_families if any(keyword in f.lower() for keyword in ['emoji', 'color', 'noto'])]
    for font in emoji_fonts:
        print(f"  - {font}")

if __name__ == '__main__':
    test_font_loading()
