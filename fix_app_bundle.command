#!/bin/bash
echo "🛠️ 修复APP包启动问题"
echo "=" * 60

APP_PATH="dist/FlexWork.app"
if [ ! -d "$APP_PATH" ]; then
    echo "❌ 错误：应用不存在，请先打包"
    exit 1
fi

echo "1. 检查当前状态..."
if [ -f "$APP_PATH/Contents/MacOS/FlexWork.bin" ]; then
    echo "   ✅ 已有备份文件"
else
    echo "   ℹ️  创建备份..."
    cp "$APP_PATH/Contents/MacOS/FlexWork" "$APP_PATH/Contents/MacOS/FlexWork.bin" 2>/dev/null || true
fi

echo -e "\n2. 修复目录结构..."
mkdir -p "$APP_PATH/Contents/Resources"
mkdir -p "$APP_PATH/Contents/MacOS"

echo -e "\n3. 创建启动脚本..."
cat > "$APP_PATH/Contents/MacOS/FlexWork" << 'SCRIPT'
#!/bin/bash
# 灵活用工平台启动脚本
cd "$(dirname "$0")/../.."
export QT_MAC_WANTS_LAYER=1
exec "$(dirname "$0")/FlexWork.bin"
SCRIPT

chmod +x "$APP_PATH/Contents/MacOS/FlexWork"
chmod +x "$APP_PATH/Contents/MacOS/FlexWork.bin" 2>/dev/null || true

echo -e "\n4. 创建Info.plist..."
cat > "$APP_PATH/Contents/Info.plist" << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>FlexWork</string>
    <key>CFBundleIdentifier</key>
    <string>com.flexwork.app</string>
    <key>CFBundleName</key>
    <string>FlexWork</string>
    <key>CFBundleDisplayName</key>
    <string>灵活用工平台</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
PLIST

echo "APPL????" > "$APP_PATH/Contents/PkgInfo"

echo -e "\n5. 修复权限..."
chmod -R 755 "$APP_PATH"
xattr -cr "$APP_PATH" 2>/dev/null || true

echo -e "\n6. 测试运行..."
echo "   从终端测试:"
"$APP_PATH/Contents/MacOS/FlexWork.bin" 2>&1 | head -5 && echo "   ✅ 可执行文件正常" || echo "   ❌ 可执行文件有问题"

echo -e "\n7. 现在可以双击测试了！"
echo "   🎯 请双击: $APP_PATH"

echo -e "\n如果双击还是不行，尝试："
echo "   A. 按住Ctrl键点击 → 打开"
echo "   B. 运行: open $APP_PATH"
echo "   C. 拖到程序坞固定"

echo -e "\n修复完成！按回车退出..."
read
