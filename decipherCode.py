import os

import PIL
import cv2
import pytesseract
from PIL import Image, ImageFilter, ImageEnhance
from skimage.measure import compare_ssim

from imageProcessing import dist, detect_digit

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class CodeDecipher():
    def __init__(self, img_path):
        self.img = img_path
        self.direction = self.get_direction()
        self.numbers = self.get_numbers()
        self.code = [self.numbers[int(self.direction[0])],
                     self.numbers[int(self.direction[1])],
                     self.numbers[int(self.direction[2])],
                     self.numbers[int(self.direction[3])]]
        print(self.direction)
        print(self.code)

    def get_numbers(self):
        numbers = []
        im = Image.open(self.img)
        columns, rows = im.size

        numbers.append(detect_digit(im.crop((0, 0, columns / 3, rows / 2))))
        numbers.append(detect_digit(im.crop((2*columns / 3, 0, columns, rows / 2))))
        numbers.append(detect_digit(im.crop((0, rows / 2, columns / 3, rows))))
        numbers.append(detect_digit(im.crop((2*columns / 3, rows / 2, columns, rows))))

        return numbers

    def get_direction(self):
        scores = []
        im1, path = self.get_arrow()
        columns, rows = im1.size
        im1 = cv2.imread(path)
        directory = './printscreens/directions/'
        for image in os.listdir(directory):
            try:
                im2 = cv2.imread(directory + '/' + image)
                (score, diff) = compare_ssim(im1, im2, full=True, multichannel=True)
                if score > 0.9:
                    scores.append([score, image[:4]])
                if score == 1.0:
                    break
            except:
                try:
                    im2 = Image.open(directory + '/' + image)
                    tmp_image = './printscreens/tmp.png'
                    tmp = im2.resize((columns, rows), resample=PIL.Image.NEAREST)
                    tmp.save(tmp_image)

                    im2 = cv2.imread(tmp_image)
                    (score, diff) = compare_ssim(im1, im2, full=True, multichannel=True)
                    if score > 0.9:
                        scores.append([score, image[:4]])
                    if score == 1.0:
                        break
                except Exception as e:
                    pass
        return scores[[x[0] for x in scores].index(max([x[0] for x in scores]))][1]

    def get_arrow(self):
        im = Image.open(self.img)

        # coloring the picture - arrow white, rest black
        pix = im.load()
        columns, rows = im.size
        for x in range(0, columns-1):
            for y in range(0, rows-1):
                if dist(pix[x, y]) < 20:
                    pix[x, y] = BLACK
                else:
                    pix[x, y] = WHITE

        # some makeup to picture
        enhance = ImageEnhance.Sharpness(im)
        im = enhance.enhance(3)
        im = im.filter(ImageFilter.MedianFilter(5))
        pix = im.load()
        columns, rows = im.size

        # cropping image to fit arrow
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

        im = im.crop(crop)
        save_at = self.img[:self.img.rfind('/')] + 'tmp_arrow.png'
        im.save(save_at)
        return im, save_at
