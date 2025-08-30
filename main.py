import os
import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTabWidget, QPushButton, QHBoxLayout, QWidget

from about_page import AboutPage
from barcode_generator import BarcodeGenerator
from qrcode_generator import QRCodeGenerator
from style import apply_material_style

'''
主程序
'''


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("计量箱建档码生成器")
        self.setGeometry(100, 100, 600, 800)
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        # 创建主布局
        main_widget = QWidget()
        main_layout = QtWidgets.QVBoxLayout(main_widget)

        self.tab_widget = QTabWidget()
        # 二维码生成
        self.qr_tab = QRCodeGenerator()
        # 条码生成
        self.barcode_tab = BarcodeGenerator()
        # 关于页面
        self.about_tab = AboutPage()

        # Tab生成
        self.tab_widget.addTab(self.barcode_tab, "条形码生成器")
        self.tab_widget.addTab(self.qr_tab, "地理位置二维码生成器")
        self.tab_widget.addTab(self.about_tab, "关于")

        main_layout.addWidget(self.tab_widget)
        self.setCentralWidget(main_widget)

    def closeEvent(self, event):
        if os.path.exists("qr_code.png"):
            os.remove("qr_code.png")
        if os.path.exists("barcode.png"):
            os.remove("barcode.png")
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # 设置应用程序图标
    app.setWindowIcon(QIcon('icon.png'))
    # 应用Material Design样式
    apply_material_style(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
