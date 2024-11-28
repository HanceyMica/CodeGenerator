from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QFrame

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

        # 创建一个容器来包含文本
        text_container = QFrame()
        text_container.setFrameStyle(QFrame.NoFrame)  # 移除边框
        text_container_layout = QVBoxLayout()
        
        # 关于文本
        about_label = QLabel(
"""
关于：
创建计量箱建档的小助手，可生成地理位置二维码、条码。
2024.03.15

更新日志：
V1.0.0.3 (2024.11.28):
1. 优化条形码生成功能。
2. 添加条形码保存功能。
3. 修复已知问题。

V1.0.0.1 (2024.11.08):
1. 修复二维码生成，显示信息对标邦手定位，信息清晰可见。
2. 修复二维码无法使用的问题。
3. 添加图标。

V0.9.0.1 (2024.03.20)
1. 更换PyQT6框架，提高程序维护难度（不是）。
2. 添加关于页面，添加二维码生成功能。
""")
        # 设置文本左对齐
        about_label.setAlignment(QtCore.Qt.AlignLeft)
        about_label.setWordWrap(True)
        
        # 将文本标签添加到容器中
        text_container_layout.addWidget(about_label)
        text_container_layout.setContentsMargins(50, 20, 50, 20)  # 设置文本容器的边距
        text_container.setLayout(text_container_layout)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(logo_label)
        main_layout.addWidget(text_container, alignment=QtCore.Qt.AlignCenter)  # 容器居中
        main_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.setLayout(main_layout)
