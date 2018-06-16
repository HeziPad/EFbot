import statistics
from skimage.measure import compare_ssim
import argparse
import imutils
import cv2
import pyautogui
import PIL
from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
from pytesseract import image_to_string
import imageProcessing
import numpy as np
import time
from skimage import img_as_float
import scipy

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'


def dist(pixel):
    max_dif = abs(pixel[0] - pixel[1])
    max_dif = max(abs(pixel[0] - pixel[2]), max_dif)
    max_dif = max(abs(pixel[1] - pixel[2]), max_dif)
    return max_dif


def detect_number():
    image = 'number9c.png'
    im = Image.open(image) # Can be many different formats.
    enhance = ImageEnhance.Sharpness(im)
    im = enhance.enhance(3)

    pix = im.load()
    columns, rows = im.size # Get the width and hight of the image for iterating over
    for x in range(columns):
        for y in range(rows):
            if dist(pix[x,y]) > 20:
                pix[x,y] = (0, 0, 0)

    save = 'number9c_d.png'
    im.save(save)  # Save the modified pixels as .png
    img = cv2.imread(save, 0)
    rows, cols = img.shape

    text = []
    for x in range(81):
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), -40 + x, 1)
        dst = cv2.warpAffine(img, M, (cols, rows))
        cv2.imwrite(save, dst)
        try:
            text.append(int(image_to_string(Image.open(save), config='-psm 10 -c tessedit_char_whitelist=0123456789')[0]))
        except:
            pass

    print(text)
    print(int(statistics.mode(text)))
    return text


def get_order(img_path):
    # time.sleep(5)
    # pyautogui.screenshot('cut_code', region=(932, 43, 60, 23))

    WHITE = (255, 255, 255)
    for each in range(1,101):

        image = './printscreens/' + str(each) + '.png'
        im = Image.open(image)
        im = im.crop((805, 255, 1115, 470))

        pix = im.load()
        columns, rows = im.size
        for x in range(0, columns-1):
            for y in range(0, rows-1):
                if dist(pix[x, y]) < 20:
                    pix[x, y] = (0, 0, 0)
                else:
                    pix[x, y] = WHITE

        save = './printscreens/directions/dir' + str(each) + '.png'
        im.save(save)
        im = Image.open(save)
        enhance = ImageEnhance.Sharpness(im)
        im = enhance.enhance(3)
        im = im.filter(ImageFilter.MedianFilter(5))
        im.save(save)

        im = Image.open(save)
        pix = im.load()
        columns, rows = im.size
        crop = [0, 0, columns, rows] # left top right bot

        cropped = False
        while not cropped:
            for x in range(columns):
                if not cropped:
                    for y in range(rows):
                        if pix[x, y] == WHITE:
                            crop[0] = x
                            cropped = True
                            break
                        else:
                            pass
                else:
                    break

        cropped = False
        while not cropped:
            for x in range(rows):
                if not cropped:
                    for y in range(columns):
                        if pix[y, x] == WHITE:
                            crop[1] = x
                            cropped = True
                            break
                        else:
                            pass
                else:
                    break

        cropped = False
        while not cropped:
            for x in reversed(range(columns)):
                if not cropped:
                    for y in range(rows):
                        if pix[x, y] == WHITE:
                            crop[2] = x
                            cropped = True
                            break
                        else:
                            pass
                else:
                    break

        cropped = False
        while not cropped:
            for x in reversed(range(rows)):
                if not cropped:
                    for y in range(columns):
                        if pix[y, x] == WHITE:
                            crop[3] = x
                            cropped = True
                            break
                        else:
                            pass
                else:
                    break
        print(crop)
        im = im.crop(crop)
        im.save(save)



def unique():
    image = './printscreens/directions/dir' + '13' + '.png'
    im1 = Image.open(image)
    columns, rows = im1.size
    im1 = cv2.imread(image)
    for each in range(1, 101):
        try:
            image = './printscreens/directions/dir' + str(each) + '.png'
            im2 = cv2.imread(image)
            (score, diff) = compare_ssim(im1, im2, full=True, multichannel=True)
            if score > 0.9:
                print(score, str(each))
        except:
            try:
                image = './printscreens/directions/dir' + str(each) + '.png'
                im2 = Image.open(image)
                tmp_image = './printscreens/tmp.png'
                tmp = im2.resize((columns, rows), resample=PIL.Image.NEAREST)
                tmp.save(tmp_image)

                im2 = cv2.imread(tmp_image)
                (score, diff) = compare_ssim(im1, im2, full=True, multichannel=True)
                if score > 0.9:
                    print(score, str(each), 'resized')
            except Exception as e:
                print('crap', e)
            pass

def decipher():
    # print screen + crop(805, 255, 1115, 470)
    im = './printscreens/1.png'
    im = Image.open(im)
    im = im.crop((805, 255, 1115, 470))
    tmp_save = './printscreens/tmp1.png'
    im.save(tmp_save)

    get_order(tmp_save)

# detect_number()
# get_order()
# unique()