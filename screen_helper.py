import subprocess

process = None

def display_image(path):
    process = subprocess.Popen(["./led-image-viewer", "--led-no-hardware-pulse", "--led-cols=64", "--led-rows=32", path])
    return process

