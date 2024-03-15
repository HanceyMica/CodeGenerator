import sys
import os
import json
import qrcode
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QWidget, QLineEdit, QComboBox, QMessageBox, QInputDialog
)
from PyQt5.QtGui import QPixmap
from datetime import datetime

class QRCodeGenerator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("二维码生成器")
        self.setGeometry(100, 100, 600, 800)  # 调整窗口大小为 600x800

        self.presets = {}
        self.load_presets()

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.preset_label = QLabel("预设：")
        self.preset_combobox = QComboBox()
        self.preset_combobox.addItems(list(self.presets.keys()))

        self.save_load_delete_layout = QHBoxLayout()  # 保存预设、加载预设、删除预设放在一行
        self.save_button = QPushButton("保存预设")
        self.save_button.clicked.connect(self.save_preset)
        self.load_button = QPushButton("加载预设")
        self.load_button.clicked.connect(self.load_preset)
        self.delete_button = QPushButton("删除预设")
        self.delete_button.clicked.connect(self.delete_preset)
        self.save_load_delete_layout.addWidget(self.save_button)
        self.save_load_delete_layout.addWidget(self.load_button)
        self.save_load_delete_layout.addWidget(self.delete_button)

        self.longitude_label = QLabel("经度：")
        self.longitude_entry = QLineEdit()
        self.latitude_label = QLabel("纬度：")
        self.latitude_entry = QLineEdit()

        self.generate_button = QPushButton("生成二维码")
        self.generate_button.clicked.connect(self.generate_qr)

        self.qr_label = QLabel()

    def create_layout(self):
        preset_layout = QHBoxLayout()  # 将「预设：」和预设下拉选择框放置在一行
        preset_layout.addWidget(self.preset_label)
        preset_layout.addWidget(self.preset_combobox)

        input_layout = QHBoxLayout()  # 经度、经度输入框、纬度、纬度输入框放在一行
        input_layout.addWidget(self.longitude_label)
        input_layout.addWidget(self.longitude_entry)
        input_layout.addWidget(self.latitude_label)
        input_layout.addWidget(self.latitude_entry)

        main_layout = QVBoxLayout()
        main_layout.addLayout(preset_layout)
        main_layout.addLayout(self.save_load_delete_layout)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.generate_button)
        main_layout.addWidget(self.qr_label)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def load_presets(self):
        try:
            with open("Presets.json", "r", encoding="utf-8") as file:
                self.presets = json.load(file)
        except FileNotFoundError:
            self.presets = {}

    def save_presets_to_file(self):
        with open("Presets.json", "w", encoding="utf-8") as file:
            json.dump(self.presets, file, ensure_ascii=False)

    def is_valid_coordinate(self, coord):
        return coord.strip() and coord.replace('.', '', 1).isdigit()

    def generate_qr(self):
        longitude = self.longitude_entry.text()
        latitude = self.latitude_entry.text()

        if not self.is_valid_coordinate(longitude) or not self.is_valid_coordinate(latitude):
            QMessageBox.warning(self, "警告", "经纬度只能是非空数字！")
            return

        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        qr_data = {"longitude": longitude, "latitude": latitude, "time": time_now, "type": "01"}
        qr_code = qrcode.make(str(qr_data))
        qr_code.save("qr_code.png")

        qr_pixmap = QPixmap("qr_code.png").scaled(300, 300)
        self.qr_label.setPixmap(qr_pixmap)
        self.qr_label.setAlignment(QtCore.Qt.AlignCenter)  # 将二维码居中显示

    def save_preset(self):
        longitude = self.longitude_entry.text()
        latitude = self.latitude_entry.text()

        if not self.is_valid_coordinate(longitude) or not self.is_valid_coordinate(latitude):
            QMessageBox.warning(self, "警告", "经纬度只能是非空数字！")
            return

        preset_name, ok = QInputDialog.getText(self, "输入预设名", "请输入预设名：")
        if ok and preset_name:
            self.presets[preset_name] = {"longitude": longitude, "latitude": latitude}
            self.save_presets_to_file()
            self.update_preset_combobox()
            QMessageBox.information(self, "成功", "预设已保存")

    def load_preset(self):
        selected_preset = self.preset_combobox.currentText()
        if selected_preset:
            self.longitude_entry.setText(self.presets[selected_preset]["longitude"])
            self.latitude_entry.setText(self.presets[selected_preset]["latitude"])

    def delete_preset(self):
        selected_preset = self.preset_combobox.currentText()
        if selected_preset in self.presets:
            del self.presets[selected_preset]
            self.save_presets_to_file()
            self.update_preset_combobox()
            QMessageBox.information(self, "成功", "预设已删除")

    def update_preset_combobox(self):
        self.preset_combobox.clear()
        self.preset_combobox.addItems(list(self.presets.keys()))

    def closeEvent(self, event):
        os.remove("qr_code.png")
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRCodeGenerator()
    window.show()
    sys.exit(app.exec_())
