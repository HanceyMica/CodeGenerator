import json
import qrcode
from datetime import datetime

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QCursor, QKeySequence
from PyQt5.QtWidgets import (
    QWidget, QLabel, QComboBox, QPushButton,
    QLineEdit, QHBoxLayout, QVBoxLayout, QMessageBox,
    QMenu, QFileDialog, QShortcut
)

'''
二维码生成页面
'''

class QRCodeGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.presets = {}
        self.load_presets()

        self.create_widgets()
        self.create_layout()


        # 设置右键菜单
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.setup_shortcuts()


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

        self.clear_button = QPushButton("清除输入框")  # 清除输入框按钮
        self.clear_button.clicked.connect(self.clear_inputs)  # 连接槽函数

        self.save_load_delete_layout.addWidget(self.save_button)
        self.save_load_delete_layout.addWidget(self.load_button)
        self.save_load_delete_layout.addWidget(self.delete_button)
        self.save_load_delete_layout.addWidget(self.clear_button)

        self.longitude_label = QLabel("经度：")
        self.longitude_entry = QLineEdit()
        self.latitude_label = QLabel("纬度：")
        self.latitude_entry = QLineEdit()

        self.generate_button = QPushButton("生成二维码")
        self.generate_button.clicked.connect(self.generate_qr)

        self.save_qr_button = QPushButton("保存二维码")
        self.save_qr_button.clicked.connect(self.save_qr_code)

        self.qr_label = QLabel()
        self.info_label = QLabel()  # 用于显示信息的标签
        self.info_label.setAlignment(QtCore.Qt.AlignLeft)  # 文本左对齐
        self.info_label.setStyleSheet("""
            QLabel {
                padding: 10px;
                margin: 0 auto;  /* 水平居中 */
                min-width: 300px;  /* 设置最小宽度 */
                max-width: 500px;  /* 设置最大宽度 */
            }
        """)

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
        main_layout.addWidget(self.generate_button) # 添加生成按钮
        main_layout.addWidget(self.save_qr_button)  # 添加保存按钮
        main_layout.addWidget(self.clear_button)    # 添加清除输入框按钮
        main_layout.addWidget(self.qr_label)        # 二维码生成label
        main_layout.addWidget(self.info_label, alignment=QtCore.Qt.AlignCenter)

        self.setLayout(main_layout)

    def show_context_menu(self, pos):
        menu = QMenu()
        save_action = menu.addAction("保存二维码")
        action = menu.exec_(QCursor.pos())

        if action == save_action:
            self.save_qr_code()

    # 清除输入框内容
    def clear_inputs(self):
        self.longitude_entry.clear()  # 清除经度输入框内容
        self.latitude_entry.clear()  # 清除纬度输入框内容

    def load_presets(self):
        try:
            with open("Presets.json", "r", encoding="utf-8") as file:
                self.presets = json.load(file)
        except FileNotFoundError:
            self.presets = {}

    def save_qr_code(self):
        """保存二维码"""
        if self.qr_label.pixmap():
            filename, _ = QFileDialog.getSaveFileName(
                self, 
                "保存二维码", 
                "", 
                "Images (*.png);;All Files (*)"
            )
            if filename:
                self.qr_label.pixmap().save(filename)
                QMessageBox.information(self, "成功", "二维码已保存")
        else:
            QMessageBox.warning(self, "警告", "无二维码，无法保存")

    def save_presets_to_file(self):
        try:
            with open("Presets.json", "w", encoding="utf-8") as file:
                json.dump(self.presets, file, ensure_ascii=False, indent=4)  # 添加缩进使JSON更易读
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存预设文件时出错：{str(e)}")

    def is_valid_coordinate(self, coord):
        """验证坐标是否有效"""
        try:
            if not coord:
                return False
                
            float_coord = float(coord)
            
            # 经度范围：-180 到 180
            # 纬度范围：-90 到 90
            # 这里使用-180到180的范围，如果是纬度可以根据需要调整
            if -180 <= float_coord <= 180:
                return True
            return False
        except ValueError:
            return False

    def generate_qr(self):
        longitude = self.longitude_entry.text()
        latitude = self.latitude_entry.text()

        if not self.is_valid_coordinate(longitude) or not self.is_valid_coordinate(latitude):
            QMessageBox.warning(self, "警告", "经纬度只能是非空数字！")
            return

        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        qr_data = {"longitude": longitude, "latitude": latitude, "time": time_now, "type": "01"}
        self.create_qr_code(qr_data)
        self.update_info_label(longitude, latitude, time_now)  # 确保在这里调用 update_info_label 方法

    def create_qr_code(self, data):
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_Q,
                box_size=10,
                border=4,
            )
            qr.add_data(str(data))
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # 使用临时文件或内存处理，避免写入磁盘
            from io import BytesIO
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            qr_pixmap = QPixmap()
            qr_pixmap.loadFromData(buffer.getvalue())
            qr_pixmap = qr_pixmap.scaled(300, 300, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            
            self.qr_label.setPixmap(qr_pixmap)
            self.qr_label.setAlignment(QtCore.Qt.AlignCenter)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成二维码时出错：{str(e)}")

    def update_info_label(self, longitude, latitude, time_now):
        # 移除制表符，使用 HTML 格式化文本
        info_text = f"""
            当前经度：{longitude}<br>
            当前纬度：{latitude}<br>
            当前时间：{time_now}
        """
        self.info_label.setText(info_text)

    def format_input(self, text):
        """格式化输入文本，移除多余空格并进行基本清理"""
        if not text:
            return ""
        return text.strip()

    def format_coordinate(self, coord):
        """格式化坐标数据，确保使用正确的小数点格式"""
        try:
            if not coord:
                return ""
            # 移除所有空格
            coord = coord.strip()
            # 将中文逗号替换为英文逗号
            coord = coord.replace('，', ',')
            # 确保使用英文小数点
            coord = coord.replace('。', '.')
            # 转换为浮点数后再转回字符串，确保格式统一
            return f"{float(coord):.6f}"  # 保留6位小数
        except ValueError:
            return coord

    def save_preset(self):
        name = self.format_input(self.preset_name_input.text())
        if not name:
            QMessageBox.warning(self, "警告", "预设名称不能为空！")
            return

        longitude = self.format_coordinate(self.longitude_input.text())
        latitude = self.format_coordinate(self.latitude_input.text())
        
        if not self.is_valid_coordinate(longitude) or not self.is_valid_coordinate(latitude):
            QMessageBox.warning(self, "警告", "请输入有效的经纬度坐标！")
            return

        self.presets[name] = {
            "longitude": longitude,
            "latitude": latitude
        }
        self.save_presets_to_file()
        self.update_preset_combobox()
        QMessageBox.information(self, "成功", "预设保存成功！")

    def load_preset(self):
        selected_preset = self.preset_combobox.currentText()
        if selected_preset:
            self.longitude_entry.setText(self.presets[selected_preset]["longitude"])
            self.latitude_entry.setText(self.presets[selected_preset]["latitude"])

    def delete_preset(self):
        selected_preset = self.preset_combobox.currentText()
        if not selected_preset:  # 检查是否有选中的预设
            QMessageBox.warning(self, "警告", "没有可删除的预设！")
            return
            
        if selected_preset in self.presets:
            reply = QMessageBox.question(
                self, 
                "确认删除", 
                f"确定要删除预设 '{selected_preset}' 吗？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                del self.presets[selected_preset]
                self.save_presets_to_file()
                self.update_preset_combobox()
                QMessageBox.information(self, "成功", "预设已删除")

    def update_preset_combobox(self):
        self.preset_combobox.clear()
        self.preset_combobox.addItems(list(self.presets.keys()))

    def setup_shortcuts(self):
        """设置快捷键"""
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self.save_qr_code)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication([])
    window = QRCodeGenerator()
    window.show()
    sys.exit(app.exec_())