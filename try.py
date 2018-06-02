def check():
    time.sleep(5)
    pyautogui.screenshot('C:/Users/Yehezkel/PycharmProjects/ef_bot/venv/Scripts/main/lvl.png', region=(932, 43, 60, 23))

    im = Image.open("C:/Users/Yehezkel/PycharmProjects/ef_bot/venv/Scripts/main/lvl.png")  # the second one 
    # im = im.filter(ImageFilter.MedianFilter())
    im = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
    enhancer = ImageEnhance.Contrast(im)
    im = im.filter(ImageFilter.MinFilter(size=1))
    im = enhancer.enhance(3)
    im = im.convert('L')
    im.save('C:/Users/Yehezkel/PycharmProjects/ef_bot/venv/Scripts/main/lvl.png')
    text = pytesseract.image_to_string(Image.open('C:/Users/Yehezkel/PycharmProjects/ef_bot/venv/Scripts/main/lvl.png') \
                                       , lang='eng', boxes=False,
                                       config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789')
    print(int(text))
