from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

# 亮色主题样式
light_style = """
    QWidget {
        font-family: 'Segoe UI', 'Microsoft YaHei';
        font-size: 18px;
    }
    
    QPushButton {
        background-color: #42A5F5;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        min-width: 88px;
        font-weight: 500;
    }
    
    QPushButton:hover {
        background-color: #2196F3;
    }
    
    QPushButton:pressed {
        background-color: #1E88E5;
    }
    
    QPushButton:disabled {
        background-color: #BDBDBD;
    }
    
    QLineEdit {
        border: 1px solid #BDBDBD;
        border-radius: 4px;
        padding: 8px;
        background: white;
    }
    
    QLineEdit:focus {
        border: 2px solid #2196F3;
    }
    
    QComboBox {
        border: 1px solid #BDBDBD;
        border-radius: 4px;
        padding: 8px;
        background: white;
    }
    
    QComboBox:drop-down {
        border: none;
        width: 20px;
    }
    
    QTabWidget::pane {
        border: none;
        background: white;
    }
    
    QTabBar::tab {
        background: #F5F5F5;
        color: #757575;
        padding: 12px 16px;
        border: none;
        min-width: 100px;
    }
    
    QTabBar::tab:selected {
        background: #2196F3;
        color: white;
    }
    
    QLabel {
        color: #212121;
    }
    
    QFrame {
        background: white;
        border-radius: 4px;
    }
"""

def apply_material_style(app):
    # 设置Material Design调色板
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255, 255, 255))
    palette.setColor(QPalette.WindowText, QColor(33, 33, 33))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
    palette.setColor(QPalette.Text, QColor(33, 33, 33))
    palette.setColor(QPalette.Button, QColor(66, 165, 245))  # Material Blue
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.Highlight, QColor(33, 150, 243))  # Material Blue
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    
    app.setPalette(palette)
    # 设置全局样式表
    app.setStyleSheet(light_style)