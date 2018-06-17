import statistics

import cv2
import numpy as np
import pyautogui
import pytesseract
from PIL import Image, ImageEnhance
from pytesseract import image_to_string

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def dist(pixel):
    max_dif = abs(pixel[0] - pixel[1])
    max_dif = max(abs(pixel[0] - pixel[2]), max_dif)
    max_dif = max(abs(pixel[1] - pixel[2]), max_dif)
    return max_dif


def detect_level():
    try:
        image = './pictures/lvl.png'
        pyautogui.screenshot(image, region=(932, 43, 60, 23))
        im = Image.open(image) # Can be many different formats.
        enhance = ImageEnhance.Sharpness(im)
        im = enhance.enhance(3)

        pix = im.load()
        columns, rows = im.size # Get the width and hight of the image for iterating over
        for x in range(columns):
            for y in range(rows):
                if dist(pix[x,y]) > 20:
                    pix[x,y] = BLACK
        im.save(image)  # Save the modified pixels as .png
        text = int(image_to_string(Image.open(image), lang='eng', boxes=False
                                   , config='-c tessedit_char_whitelist=0123456789'))
        return text
    except:
        return 0


def detect_digit(im):
    """rotates an image by +-40 degrees and returns the single detected digit"""
    enhance = ImageEnhance.Sharpness(im)
    im = enhance.enhance(3)

    pix = im.load()
    columns, rows = im.size # Get the width and height of the image for iterating over
    for x in range(columns):
        for y in range(rows):
            if np.mean(pix[x,y]) > 130:
                pix[x,y] = WHITE
            else:
                pix[x, y] = BLACK

    tmp_save = 'tmp_detect_number.png'
    im.save(tmp_save)

    img = cv2.imread(tmp_save, 0)
    rows, cols = img.shape

    text = []
    degs = 40
    for x in range(int((2*degs+1)/3)):
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), -degs + 3*x, 1)
        dst = cv2.warpAffine(img, M, (cols, rows))
        cv2.imwrite(tmp_save, dst)
        try:
            text.append(int(image_to_string(Image.open(tmp_save), config='-psm 10 -c tessedit_char_whitelist=0123456789')[0]))
        except:
            pass
    counter = False
    while True:
        try:
            return int(statistics.mode(text))
        except:
            counter = not counter
            text.pop(len(text)-1) if counter else text.pop(0)


def image_search(image, region, precision=0.94):
    """Searches for an image within an area, with precision
    image: path to the image file (see opencv imread for supported types)
    region: x, y, width, height
    precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8
    returns :
    the coordinates (x,y) of max match"""
    x1, y1, width, height = region[0], region[1], region[2], region[3]
    im = pyautogui.screenshot(region=(x1, y1, width, height))

    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return None
    return max_loc[0]+x1, max_loc[1]+y1
