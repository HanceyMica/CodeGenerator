import barcode
from barcode.writer import ImageWriter
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QWidget, QLineEdit, QMessageBox, QMenu, QFileDialog
)
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image

'''
条码生成页面
'''


class BarcodeGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("请输入条形码号：")
        self.entry = QLineEdit()
        self.generate_button = QPushButton("生成条形码")
        self.barcode_image = QLabel()

        self.setup_ui()
        self.setup_actions()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.label)
        input_layout.addWidget(self.entry)

        layout.addLayout(input_layout)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.barcode_image)

        # 绑定右键菜单
        self.barcode_image.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.barcode_image.customContextMenuRequested.connect(self.show_context_menu)

    def setup_actions(self):
        self.generate_button.clicked.connect(self.generate_barcode)

    def show_context_menu(self, pos):
        menu = QMenu(self)
        paste_action = menu.addAction("粘贴")
        paste_action.triggered.connect(self.paste_text)
        save_action = menu.addAction("保存条形码")
        save_action.triggered.connect(self.save_barcode)
        menu.exec_(self.barcode_image.mapToGlobal(pos))

    def paste_text(self):
        clipboard_text = QApplication.clipboard().text()
        self.entry.setText(clipboard_text)

    def generate_barcode(self):
        barcode_number = self.entry.text()
        if barcode_number:
            try:
                code128 = barcode.get_barcode_class('code128')
                barcode_instance = code128(barcode_number, writer=ImageWriter())
                filename = barcode_instance.save('barcode')
                barcode_image = Image.open(filename)

                # Convert PIL image to QImage
                qimage = QImage(barcode_image.tobytes(),
                                barcode_image.width,
                                barcode_image.height,
                                barcode_image.width * 3,
                                QImage.Format_RGB888)

                # barcode_pixmap = QPixmap.fromImage(qimage.convertToFormat(QImage.Format_RGB888))
                barcode_pixmap = QPixmap.fromImage(qimage)
                self.barcode_image.setPixmap(barcode_pixmap)
                self.barcode_image.setAlignment(QtCore.Qt.AlignCenter)  # 将条形码居中显示

            except Exception as e:
                QMessageBox.critical(self, "Error", f"生成条形码时出现错误：{str(e)}")
        else:
            QMessageBox.critical(self, "Error", "请输入条形码号")

    def save_barcode(self):
        barcode_number = self.entry.text()
        if barcode_number:
            filename, _ = QFileDialog.getSaveFileName(self, "保存条形码", "", "PNG files (*.png)")
            if filename:
                try:
                    code128 = barcode.get_barcode_class('code128')
                    barcode_instance = code128(barcode_number, writer=ImageWriter())
                    barcode_instance.save(filename)
                    QMessageBox.information(self, "Success", "条形码已保存成功！")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"保存条形码时出现错误：{str(e)}")
        else:
            QMessageBox.critical(self, "Error", "请输入条形码号")
