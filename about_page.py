from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget

'''
关于页面
'''


class AboutPage(QWidget):
    def __init__(self):
        super().__init__()

        about_label = QLabel("关于：\n创建计量箱建档的小助手。\n2024.03.15")
        about_label.setAlignment(QtCore.Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(about_label)

        self.setLayout(layout)
