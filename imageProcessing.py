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
    while True:
        try:
            return int(statistics.mode(text))
        except:
            text.pop(int(len(text)/2))


def region_grabber(region):
    '''grabs a region (topx, topy, bottomx, bottomy)
    to the tuple (topx, topy, width, height)
    input : a tuple containing the 4 coordinates of the region to capture
    output : a PIL image of the area selected.'''
    x1 = region[0]
    y1 = region[1]
    width = region[2]-x1
    height = region[3]-y1

    return pyautogui.screenshot(region=(x1,y1,width,height))


def imagesearcharea(image, x1,y1,x2,y2, precision=0.8, im=None) :
    '''Searches for an image within an area
    input :
    image : path to the image file (see opencv imread for supported types)
    x1 : top left x value
    y1 : top left y value
    x2 : bottom right x value
    y2 : bottom right y value
    precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8
    im : a PIL image, usefull if you intend to search the same unchanging region for several elements
    returns :
    the top left corner coordinates of the element if found as an array [x,y] or [-1,-1] if not'''
    if im is None :
        im = region_grabber(region=(x1, y1, x2, y2))

    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc[0]+x1, max_loc[1]+y1

