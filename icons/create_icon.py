from PIL import Image, ImageDraw, ImageFont
import os

# 创建1024x1024的图片
img = Image.new('RGB', (1024, 1024), color='#007AFF')
draw = ImageDraw.Draw(img)

# 画一个圆形背景
draw.ellipse([100, 100, 924, 924], fill='#0056CC')

# 添加文字（需要字体，这里简单画个形状）
draw.rectangle([400, 400, 624, 624], fill='white')
draw.rectangle([450, 450, 574, 574], fill='#007AFF')

img.save('app_icon.png')
print("图标已创建: app_icon.png")
