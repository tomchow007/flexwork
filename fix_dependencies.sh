#!/bin/bash
echo "修复依赖问题..."

# 1. 创建虚拟环境
python3 -m venv venv_fix
source venv_fix/bin/activate

# 2. 安装所有依赖
pip install PyQt6 pandas openpyxl

# 3. 在虚拟环境中重新打包
python -m PyInstaller --windowed --name="FlexWork" app.py

# 4. 复制到dist目录
if [ -d "dist/FlexWork.app" ]; then
    cp -r dist/FlexWork.app ../FlexWork_fixed.app
    echo "✅ 修复完成: FlexWork_fixed.app"
fi

deactivate
