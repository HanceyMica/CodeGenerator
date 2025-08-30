# 计量箱建档码生成器 - Go技术栈实现提示词


## 项目概述
请使用Go技术栈实现一个计量箱建档码生成器桌面客户端程序，具有条形码和二维码生成功能。该应用应当保持原有的功能特性，同时利用Go的优势提供更好的性能和可维护性。

## 技术栈选择
- GUI框架：Fyne (fyne.io/fyne/v2)
- 条形码生成：boombuler/barcode
- 二维码生成：skip2/go-qrcode
- 主题：Fyne Material Design主题
- 配置管理：encoding/json

## 项目结构
```
/
├── cmd/
│   └── main.go           # 应用入口点
├── internal/
│   ├── ui/              # 用户界面组件
│   │   ├── window.go     # 主窗口设置
│   │   ├── barcode.go    # 条形码标签页
│   │   ├── qrcode.go     # 二维码标签页
│   │   └── about.go      # 关于页面
│   ├── models/           # 数据模型
│   │   └── preset.go     # 预设配置模型
│   └── utils/            # 工具函数
│       └── generator.go  # 码生成工具
├── assets/              # 应用资源
│   ├── icons/           # 图标资源
│   └── theme/           # 主题资源
└── go.mod               # Go模块定义
```

## 核心功能实现

### 1. 主程序入口 (cmd/main.go)
```go
func main() {
    app := app.New()
    app.Settings().SetTheme(theme.DefaultTheme())
    
    mainWindow := window.NewMainWindow(app)
    mainWindow.Resize(fyne.NewSize(1280, 720))
    
    mainWindow.ShowAndRun()
}
```

### 2. 条形码生成器 (internal/ui/barcode.go)
- 实现条形码生成界面
- 支持Code128格式
- 提供预览和保存功能
- 实现输入验证
- 复制到剪贴板功能

### 3. 二维码生成器 (internal/ui/qrcode.go)
- 实现地理位置二维码生成
- 支持预设管理（保存、加载、删除）
- 提供经纬度输入和验证
- 实现二维码图片生成和保存
- 复制到剪贴板功能

### 4. 用户界面设计
- 使用Material Design风格的Fyne主题
- 实现标签页式布局
- 提供直观的用户交互
- 支持键盘快捷键
- 适配深色/浅色主题

## 数据管理
- 使用JSON文件存储预设数据
- 实现简单的文件锁机制避免并发访问问题
- 支持导入/导出预设配置

## 安全考虑
- 实现输入验证和清理
- 安全的文件操作方式
- 实现适当的错误处理和日志记录

## 打包部署
- 提供跨平台编译脚本
- 支持Windows、macOS和Linux平台
- 实现单文件发布
- 提供安装包生成配置

## 扩展建议
- 添加批量生成功能
- 支持更多条码格式
- 添加图片水印功能
- 实现条码扫描识别功能
- 支持自定义主题