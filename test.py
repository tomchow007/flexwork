print("=" * 50)
print("Python环境测试")
print("=" * 50)
print("1. Python版本检查...")
import sys
print(f"Python版本: {sys.version}")
print()
print("2. 尝试导入PyQt6...")
try:
    from PyQt6.QtWidgets import QApplication
    print("✅ PyQt6导入成功！")
except ImportError as e:
    print(f"❌ PyQt6导入失败: {e}")
    print("请运行: pip3 install PyQt6")
print()
print("3. 测试完成！")
print("=" * 50)
