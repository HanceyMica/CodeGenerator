import os
import tempfile

import barcode
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QKeySequence
from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QWidget, QLineEdit, QMessageBox, QMenu, QFileDialog,
    QShortcut
)
from barcode.writer import ImageWriter

'''
条码生成页面
'''


class BarcodeGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("请输入条形码号：")
        self.entry = QLineEdit()
        self.generate_button = QPushButton("生成条形码")
        self.save_button = QPushButton("保存条形码")
        self.clear_button = QPushButton("清空")
        self.barcode_image = QLabel()

        self.setup_ui()
        self.setup_actions()
        self.setup_shortcuts()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.label)
        input_layout.addWidget(self.entry)
        input_layout.addWidget(self.clear_button)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.save_button)

        layout.addLayout(input_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.barcode_image)

        self.save_button.setEnabled(False)

        self.barcode_image.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.barcode_image.customContextMenuRequested.connect(self.show_context_menu)

    def setup_actions(self):
        self.generate_button.clicked.connect(self.generate_barcode)
        self.save_button.clicked.connect(self.save_barcode)
        self.clear_button.clicked.connect(self.clear_input)
        self.entry.textChanged.connect(self.on_text_changed)
        self.entry.returnPressed.connect(self.generate_barcode)

    def setup_shortcuts(self):
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self.save_barcode)

    def clear_input(self):
        self.entry.clear()
        self.barcode_image.clear()
        self.save_button.setEnabled(False)

    def on_text_changed(self):
        has_text = bool(self.entry.text().strip())
        self.generate_button.setEnabled(has_text)

    def generate_barcode(self):
        barcode_number = self.entry.text().strip()
        if not barcode_number:
            QMessageBox.critical(self, "错误", "请输入条形码号")
            return
            
        try:
            writer = ImageWriter()
            writer.set_options({
                'module_height': 50.0,     # 增加高度使条码更清晰
                'module_width': 1.0,      # 调整宽度以适应长数字
                'quiet_zone': 10.0,        # 增加两侧留白
                'font_size': 10.00,           # 增加字体大小
                'text_distance': 5.0,
                'write_text': True
            })
            
            code128 = barcode.get_barcode_class('code128')
            barcode_instance = code128(barcode_number, writer=writer)
            
            temp_dir = tempfile.gettempdir()
            temp_filename = os.path.join(temp_dir, f'barcode_{barcode_number}')
            
            filename = barcode_instance.save(temp_filename)
            
            barcode_pixmap = QPixmap(filename)
            scaled_pixmap = barcode_pixmap.scaled(
                1000, 400,  # 增加显示尺寸以适应长条码
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
            
            self.barcode_image.setPixmap(scaled_pixmap)
            self.barcode_image.setAlignment(QtCore.Qt.AlignCenter)
            
            self.save_button.setEnabled(True)
            
            try:
                os.remove(filename)
            except:
                pass

        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成条形码时出现错误：{str(e)}")
            self.save_button.setEnabled(False)

    def save_barcode(self):
        barcode_number = self.entry.text().strip()
        if not barcode_number:
            QMessageBox.critical(self, "错误", "请输入条形码号")
            return
            
        filename, _ = QFileDialog.getSaveFileName(
            self, 
            "保存条形码", 
            f"barcode_{barcode_number}.png",
            "PNG files (*.png)"
        )
        
        if filename:
            try:
                writer = ImageWriter()
                writer.set_options({
                    'module_height': 50.0,     # 与生成时保持一致
                    'module_width': 1.0,      # 与生成时保持一致
                    'quiet_zone': 10.0,        # 与生成时保持一致
                    'font_size': 10.00,           # 与生成时保持一致
                    'text_distance': 5.0,
                    'write_text': True
                })
                
                code128 = barcode.get_barcode_class('code128')
                barcode_instance = code128(barcode_number, writer=writer)
                barcode_instance.save(filename)
                QMessageBox.information(self, "成功", "条形码已保存成功！")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存条形码时出现错误：{str(e)}")

    def show_context_menu(self, pos):
        menu = QMenu(self)
        paste_action = menu.addAction("粘贴")
        paste_action.triggered.connect(self.paste_text)
        clear_action = menu.addAction("清空")
        clear_action.triggered.connect(self.clear_input)
        if self.barcode_image.pixmap():
            save_action = menu.addAction("保存条形码")
            save_action.triggered.connect(self.save_barcode)
        menu.exec_(self.barcode_image.mapToGlobal(pos))

    def paste_text(self):
        clipboard_text = QApplication.clipboard().text()
        self.entry.setText(clipboard_text)
