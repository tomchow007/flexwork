from PIL import Image, ImageDraw
img = Image.new('RGBA', (256, 256), (255, 255, 255, 0))
draw = ImageDraw.Draw(img)
draw.ellipse([20, 20, 236, 236], fill=(0, 122, 255))
draw.rectangle([100, 100, 156, 156], fill=(255, 255, 255))
img.save('dist/FlexWork.app/Contents/Resources/AppIcon.icns')
