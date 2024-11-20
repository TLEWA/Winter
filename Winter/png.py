from PIL import Image
from tools import *

def init_png(str,width,height,x,y):
    print(str)
    png = Image.open(str)
    return PNG(png, width, height, x, y)