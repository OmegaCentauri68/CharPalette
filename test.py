# test.py
# For testing only
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QFrame, QTabWidget, QGridLayout
import sys
from utils import *

class Demo(QWidget):
    def __init__(self):
        super().__init__()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(QLabel("Ô 0,0"), 0, 0)
        grid.addWidget(QPushButton("Nút 0,1"), 0, 1)
        grid.addWidget(QLabel("Ô 1,0"), 1, 0)
        grid.addWidget(QPushButton("Nút to chiếm 2 cột"), 1, 1, 1, 2)
        grid.addWidget(QLabel("Ô 2,0"), 2, 0)
        grid.addWidget(QPushButton("Ô 2,2"), 2, 2)

        self.setLayout(grid)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    sys.exit(app.exec())