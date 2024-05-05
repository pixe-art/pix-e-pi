import subprocess
from PIL import Image, ImageDraw, ImageFont

process = None

def display_image(path):
    process = subprocess.Popen(["./led-image-viewer", "--led-cols=64", "--led-rows=32", path])
    return process

def generate_pairing_image(code):
    width, height = 64, 32

    text = str(code)
    font = ImageFont.truetype("arial.ttf", 20)

    image = Image.new('RGB', (width, height), 'black')
    draw = ImageDraw.Draw(image)
    _, _, w, h = draw.textbbox((0, 0), text, font=font)
    draw.text(((width-w)/2, ((height-h)/2)-2), text, font=font, fill='white')

    image.save('pairing_image.png')
