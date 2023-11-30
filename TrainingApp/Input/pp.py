import sys
from PyQt5.QtGui import QColor, QFont
import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLabel, QFileDialog, QLineEdit, QRadioButton, \
    QPlainTextEdit


class EvalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle('Оценка данных')

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EvalApp()
    sys.exit(app.exec_())
