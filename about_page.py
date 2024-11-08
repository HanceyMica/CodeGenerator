from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget

'''
关于页面
'''


class AboutPage(QWidget):
    def __init__(self):
        super().__init__()

        logo_label = QLabel()
        logo_pixmap = QPixmap("icon.png").scaled(300, 300)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(QtCore.Qt.AlignCenter)

        about_label = QLabel(
"""
    关于：
    创建计量箱建档的小助手，可生成地理位置二维码、条码。
    2024.03.15
    
    更新日志：
    V0.9.0.1 (2024.03.20)
    1. 更换PyQT6框架，提高程序维护难度（不是）。
    2. 添加关于页面，添加二维码生成功能。
    
    V1.0.0.1 (2024.11.08):
    1. 修复二维码生成，显示信息对标邦手定位，信息清晰可见。
    2. 修复二维码无法使用的问题。
    3. 添加图标。
""")
        about_label.setAlignment(QtCore.Qt.AlignLeft)

        layout = QVBoxLayout()
        layout.addWidget(logo_label)
        layout.addWidget(about_label)

        self.setLayout(layout)
