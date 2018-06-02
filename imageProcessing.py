import statistics
import subprocess
from PIL import ImageGrab
import cv2
import numpy as np
from numpy import array
import time
import pyautogui
from threading import Timer
from pynput import keyboard
import sys
from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
from pytesseract import image_to_string
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'


def dist(pixel):
    max_dif = abs(pixel[0] - pixel[1])
    max_dif = max(abs(pixel[0] - pixel[2]), max_dif)
    max_dif = max(abs(pixel[1] - pixel[2]), max_dif)
    return max_dif


def detect_level():
    image = 'lvl.png'
    pyautogui.screenshot(image, region=(932, 43, 60, 23))
    im = Image.open(image) # Can be many different formats.
    enhance = ImageEnhance.Sharpness(im)
    im = enhance.enhance(3)

    pix = im.load()
    columns, rows = im.size # Get the width and hight of the image for iterating over
    for x in range(columns):
        for y in range(rows):
            if dist(pix[x,y]) > 20:
                pix[x,y] = (0, 0, 0)
    im.save(image)  # Save the modified pixels as .png
    text = int(image_to_string(Image.open(image), lang='eng', boxes=False, config='--psm 8 tessedit_char_whitelist '                                                                   '0123456789'))
    print(text)
    return text
