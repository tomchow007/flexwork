import sys
import os
import subprocess

print("=" * 60)
print("环境诊断报告")
print("=" * 60)

# 1. 系统信息
print("1. 系统信息:")
print(f"   平台: {sys.platform}")
print(f"   Python路径: {sys.executable}")
print(f"   Python版本: {sys.version}")

# 2. PATH环境变量
print("\n2. PATH环境变量:")
paths = os.environ.get('PATH', '').split(':')
for path in paths[:10]:  # 只显示前10个
    print(f"   {path}")

# 3. 检查pip安装的包
print("\n3. 尝试导入PyInstaller:")
try:
    import PyInstaller
    print(f"   ✅ PyInstaller可导入: {PyInstaller.__version__}")
    
    # 查找可执行文件
    import site
    for path in site.getsitepackages():
        pyinstaller_path = os.path.join(path, 'PyInstaller', '__main__.py')
        if os.path.exists(pyinstaller_path):
            print(f"   PyInstaller模块位置: {pyinstaller_path}")
            
except ImportError as e:
    print(f"   ❌ PyInstaller导入失败: {e}")

# 4. 检查PyQt6
print("\n4. 检查PyQt6:")
try:
    import PyQt6
    print(f"   ✅ PyQt6可导入")
except ImportError as e:
    print(f"   ❌ PyQt6导入失败: {e}")

# 5. 建议
print("\n5. 建议解决方案:")
print("   A. 使用完整路径运行:")
print(f"      {sys.executable} -m PyInstaller --windowed app.py")
print("   B. 或创建.command文件（最简单）")
print("   C. 或重新安装: pip3 install --user pyinstaller")

print("=" * 60)
