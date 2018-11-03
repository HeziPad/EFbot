import statistics
import sys
import time
from threading import Timer
import subprocess

import pyautogui
import pytesseract
from pynput import keyboard

from imageProcessing import detect_level, image_search
from myemail import send_gmail
from decipherCode import CodeDecipher

import logging

tmp_time = time.time()

while time.time() - tmp_time < 180:
    try:
        x, y = pyautogui.locateCenterOnScreen('./pictures/AccessRewardConfirm.png', region=(900, 830, 120, 50))
        print('AccessRewardConfirm found')
        pyautogui.click(x, y)
        time.sleep(2)
    except Exception as e:
        print('AccessRewardConfirm NOT found {}'.format(e))

    try:
        x, y = pyautogui.locateCenterOnScreen('./pictures/Distortion2Confirm.png', region=(900, 900, 120, 60))
        print('Distortion2Confirm found')
        pyautogui.click(x, y)
        time.sleep(2)
    except Exception as e:
        print('Distortion2Confirm NOT found {}'.format(e))

    try:
        x, y = pyautogui.locateCenterOnScreen('./pictures/startConfirm.png', region=(900, 870, 120, 60))
        print('startConfirm found')
        pyautogui.click(x, y)
        time.sleep(2)
    except Exception as e:
        print('startConfirm NOT found {}'.format(e))

    try:
        x, y = pyautogui.locateCenterOnScreen('./pictures/XNews.png', region=(1150, 840, 50, 50))
        print('XNews found')
        pyautogui.click(x, y)
        time.sleep(2)
    except Exception as e:
        print('XNews NOT found {}'.format(e))