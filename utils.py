# utils.py
from typing import TypeVar, overload
from PySide6.QtCore import QSize, Qt, QObject, QMargins, QPoint, QRect
from PySide6.QtWidgets import QApplication, QLayout, QFrame, QWidget, QSizePolicy
from PySide6.QtGui import QFont
from typing import TypedDict
from grapheme import graphemes
import yaml
import os
import sys

T = TypeVar('T', bound=QWidget)
L = TypeVar('L', bound=QLayout)

class FlowLayout(QLayout):
    def __init__(self, parent=None):
        super().__init__(parent)

        if parent is not None:
            self.setContentsMargins(QMargins(0, 0, 0, 0))

        self._item_list = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self._item_list.append(item)

    def count(self):
        return len(self._item_list)

    def itemAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list[index]

        return None

    def takeAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list.pop(index)

        return None

    def expandingDirections(self):
        return Qt.Orientation(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self._do_layout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self._do_layout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self._item_list:
            size = size.expandedTo(item.minimumSize())

        size += QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size

    def _do_layout(self, rect, test_only):
        if not self._item_list:
            return 0

        spacing = self.spacing()

        # First pass: calculate line breaks and line widths
        lines = []
        current_line = []
        current_line_width = 0
        line_height = 0

        for item in self._item_list:
            style = item.widget().style()
            layout_spacing_x = style.layoutSpacing(
                QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal
            )
            layout_spacing_y = style.layoutSpacing(
                QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical
            )
            space_x = spacing + layout_spacing_x
            space_y = spacing + layout_spacing_y

            item_width = item.sizeHint().width()
            item_height = item.sizeHint().height()

            # Check if we need to wrap to next line
            needed_width = current_line_width + (space_x if current_line else 0) + item_width
            if needed_width > rect.width() and current_line:
                # Save current line and start new one
                lines.append({
                    'items': current_line.copy(),
                    'width': current_line_width,
                    'height': line_height,
                    'space_y': space_y
                })
                current_line = [item]
                current_line_width = item_width
                line_height = item_height
            else:
                # Add to current line
                if current_line:
                    current_line_width += space_x
                current_line.append(item)
                current_line_width += item_width
                line_height = max(line_height, item_height)

        # Don't forget the last line
        if current_line:
            lines.append({
                'items': current_line.copy(),
                'width': current_line_width,
                'height': line_height,
                'space_y': spacing + (lines[0]['space_y'] if lines else 0)
            })

        # Second pass: position items with centering
        if not test_only:
            y = rect.y()
            for line in lines:
                # Calculate x offset to center the line
                available_width = rect.width()
                line_width = line['width']
                x_offset = rect.x() + (available_width - line_width) // 2

                x = x_offset
                for i, item in enumerate(line['items']):
                    item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

                    # Add spacing for next item (except for last item)
                    if i < len(line['items']) - 1:
                        style = item.widget().style()
                        layout_spacing_x = style.layoutSpacing(
                            QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal
                        )
                        space_x = spacing + layout_spacing_x
                        x += item.sizeHint().width() + space_x
                    else:
                        x += item.sizeHint().width()

                y += line['height'] + line['space_y']

        # Calculate total height
        total_height = sum(line['height'] for line in lines)
        if len(lines) > 1:
            total_height += sum(line['space_y'] for line in lines[1:])

        return total_height

class TabConfig(TypedDict):
    tab_name: str
    font: str
    path: str

@overload
def create_widget(widget_class: type[T], layout_class: None = None, text: str|None = None, object_name: str|None = None) -> T: ...
@overload
def create_widget(widget_class: type[T], layout_class: type[L], text: str|None = None, object_name: str|None = None) -> tuple[T, L]: ...

def create_widget(widget_class: type[T], layout_class: type[L]|None = None, text: str|None = None, object_name: str|None = None) -> T | tuple[T, L]:
    """Quickly create widget and set layout"""
    widget = widget_class()
    if layout_class is not None:
        layout = layout_class()
        widget.setLayout(layout)
    if object_name is not None: widget.setObjectName(object_name)
    if text is not None and hasattr(widget, 'setText'):
        widget.setText(text)

    if layout_class:
        return widget, layout
    else:
        return widget

def create_layout(widget: QWidget, layout_class: type[L]) -> L:
    """Quickly create and set layout"""
    layout = layout_class()
    widget.setLayout(layout)
    return layout

def add_widgets(self: QLayout, *widgets: QWidget) -> None:
    for widget in widgets:
        self.addWidget(widget)

def change_font_weight(widget: T, font_weight: QFont.Weight) -> None:
    font = widget.font()
    font.setWeight(font_weight)
    widget.setFont(font)

def load_qss(app: QApplication, file_path: str) -> None:
    path = get_resource_path(file_path)
    with open(path, 'r') as file:
        app.setStyleSheet(file.read())

def get_yaml_data(file_path: str) -> list[TabConfig]:
    absolute_path = get_resource_path(file_path)
    with open(absolute_path, 'r', encoding='utf-8') as file:
        data: list[TabConfig] = yaml.safe_load(file)
    return data

def get_tab_file_data(file_path: str) -> tuple[str, ...]:
    path = get_resource_path(file_path)
    with open(path, 'r', encoding='utf-8') as f:
        content: str = f.read()
        return tuple(g for g in graphemes(content) if not g.isspace())

def get_resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

QLayout.add_widgets = add_widgets