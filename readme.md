# 计量箱建档码生成器

一个基于 `PyQt5` 的计量箱建档工具,可以生成地理位置二维码和条形码。

## 功能特点

- 生成地理位置二维码
  - 支持经纬度坐标输入
  - 支持预设位置保存和加载
  - 二维码图片可保存
  
- 生成条形码
  - 支持 Code128 格式条形码生成
  - 条码图片可保存

- 其他功能
  - 支持快捷键操作(Ctrl+S保存条形码、二维码)
  - 右键菜单支持
  - 友好的用户界面

## 安装说明

1. 克隆仓库到本地:
```bash
git clone https://github.com/HanceyMica/CodeGenerator.git
```

2. 安装依赖:（如不需要打包，可在requirements.txt中删除cx_Freeze）

```bash
pip install -r requirements.txt
```

3. 运行程序:
```bash
python main.py
```
## 打包说明（可选）

使用`cx_Freeze`进行打包, 在`requirements.txt`中删除`cx_Freeze`后，可跳过此步骤:

```bash
python setup.py build
```

## 系统要求

- Python 3.8+
- Windows 操作系统 (已测试)

## 版本历史

### V1.0.0.3 (2024.11.28)
- 优化条形码生成功能
- 添加条形码保存功能
- 修复已知问题

### V1.0.0.1 (2024.11.08)
- 修复二维码生成显示
- 修复二维码使用问题
- 添加程序图标

### V0.9.0.1 (2024.03.20)
- 更换为 PyQt5 框架
- 添加关于页面
- 添加二维码生成功能

## 许可证

本项目基于 `MIT` 许可证开源。