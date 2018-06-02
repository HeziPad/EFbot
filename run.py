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
from myemail import send_gmail

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'


# #Makes Full Screen
# try:
#     x,y = pyautogui.locateCenterOnScreen('full_screen.png')
#     pyautogui.click(x, y)
# except:
#     print 'Nox didn\'t open'

# Open Endless Frontier
# def openGame():
#     try:
#         x,y = pyautogui.locateCenterOnScreen('endless_frontier.png')
#         pyautogui.click(x, y)
#         loading = True
#         while(loading):
#             time.sleep(2)
#             try:
#                 x,y = pyautogui.locateCenterOnScreen('open_game_confirm.png')
#                 pyautogui.click(x, y)
#                 loading = False
#             except:
#                 try:
#                     x,y = pyautogui.locateCenterOnScreen('dont_show.png')
#                     pyautogui.click(x, y)
#                     time.sleep(1)
#                     x,y = pyautogui.locateCenterOnScreen('open_game_x.png')
#                     pyautogui.click(x, y)
#                     loading = False
#                 except:
#                     try:
#                         x,y = pyautogui.locateCenterOnScreen('medal_check.png')
#                         pyautogui.click(x, y)
#                         loading = False
#                     except:
#                         pass
#         time.sleep(3)
#         try:
#             x,y = pyautogui.locateCenterOnScreen('dont_show.png')
#             pyautogui.click(x, y)
#             time.sleep(1)
#             x,y = pyautogui.locateCenterOnScreen('open_game_x.png')
#             pyautogui.click(x, y)
#             time.sleep(3)
#         except:
#             pass
#     except:
#         print 'Endless Frontier didn\'t open'

# def closeGame():
#     x,y = pyautogui.locateCenterOnScreen('minimize_game.png')
#     pyautogui.click(x, y)
#     time.sleep(3)
#     x,y = pyautogui.locateCenterOnScreen('minimize_game_logo.png')
#     pyautogui.mouseDown(x, y, button='left')
#     pyautogui.moveRel(-300, 0, 1.5)
#     pyautogui.mouseUp(x-300, y, button='left')
#     time.sleep(2)

class wR():
    is_reopen_game = False
    is_revive = False
    is_open_chests = False
    is_max_quests = False
    is_buy_units = False
    is_upgrade_units = False
    exiting = False
    delay = 0.5
    delay_small = 0.1

    level_check_time = time.time()
    level_filter = [1] * 50
    level = 1
    check_number = 0
    open_chests_counter = 0
    max_quests_counter = 0
    quests_add_rel = 0
    distortion_passed = False
    upgraded_units_once = False
    max_level_reached = False

    def startTimer(self):
        self.skills_timer = Timer(2, use_skills)
        self.skills_timer.start()
        self.open_chests_timer = Timer(3, open_chests)
        self.open_chests_timer.start()
        self.max_quests_timer = Timer(4, max_quests)
        self.max_quests_timer.start()
        self.upgrade_units_timer = Timer(8 * 60, upgrade_units)
        self.upgrade_units_timer.start()
        self.buy_units_timer = Timer(2 * 60, buy_units)
        self.buy_units_timer.start()

    def stopTimer(self):
        self.skills_timer.cancel()
        self.open_chests_timer.cancel()
        self.max_quests_timer.cancel()
        self.upgrade_units_timer.cancel()
        self.buy_units_timer.cancel()


# def arenaBattle():
#     if(wR.exiting):
#         return
#     wR.arenaBattling = True
#     if(not wR.buyingUnits and not wR.upgradingUnits and not wR.xSpeeding and not wR.reviving and not wR.questing):
#         print 'Battling in Arena'
#         pyautogui.click(1083, 991)#Clicks battle
#         time.sleep(2)
#         pyautogui.click(1147, 589)#Enters Battle Arena
#         try:
#             x,y = pyautogui.locateCenterOnScreen('battle_arena_confirm.png')
#             pyautogui.click(x, y)
#             time.sleep(1)
#             pyautogui.click(706, 992)#Back to quests
#             wR.arenaBattling = False
#             wR.arenaBattleTimer = Timer(60*30, arenaBattle)
#             wR.arenaBattleTimer.start()
#         except:
#             pass
#         time.sleep(2)
#         while(wR.arenaBattling):
#             try:
#                 time.sleep(5)
#                 x,y = pyautogui.locateCenterOnScreen('0_battle.png')
#                 print 'zero battles'
#                 pyautogui.click(1189, 222)#Hits x
#                 time.sleep(2)
#                 pyautogui.click(706, 992)#Back to quests
#                 wR.arenaBattling = False
#                 wR.arenaBattleTimer = Timer(60*30, arenaBattle)
#                 wR.arenaBattleTimer.start()
#             except:
#                 pyautogui.click(1066, 880)#Hits Battle
#                 battling = True
#                 while(battling):
#                     time.sleep(2)
#                     try:
#                         x,y = pyautogui.locateCenterOnScreen('battle_arena_confirm.png')
#                         pyautogui.click(x, y)#Hits Confirm
#                         time.sleep(1)
#                         battling = False
#                     except:
#                         pass
#                     try:
#                         x,y = pyautogui.locateCenterOnScreen('battle_arena_confirm2.png')
#                         pyautogui.click(x, y)#Hits Confirm
#                         time.sleep(1)
#                         battling = False
#                     except:
#                         pass
#         print 'Finished Battling in Arena'
#     else:
#         wR.arenaBattleTimer = Timer(20, arenaBattle)
#         wR.arenaBattleTimer.start()

# def buyUnit():
#     if(wR.exiting):
#         return
#     wR.buyingUnits = True
#     if(not wR.arenaBattling and not wR.upgradingUnits and not wR.xSpeeding and not wR.reviving and not wR.questing):
#         print 'Buying Units'
#         pyautogui.click(800, 1000)#Clicks unit
#         time.sleep(1)
#         pyautogui.click(1141, 508)#Clicks buy unit
#         try:
#             x,y = pyautogui.locateCenterOnScreen('refresh_unit.png')
#             pyautogui.click(x, y)
#             time.sleep(1)
#             try:
#                 x,y = pyautogui.locateCenterOnScreen('cacel.png')
#                 pyautogui.click(x, y)
#             except:
#                 pass
#             for i in xrange(4):
#                 print 'Bought Unit:', i+1
#                 time.sleep(3)
#                 x,y = pyautogui.locateCenterOnScreen('unit_medal.png')
#                 pyautogui.click(x, y)
#                 time.sleep(1)
#                 pyautogui.click(928, 720)#Send unit to time shop
#
#             wR.buyUnitTimer = Timer(30*60, buyUnit)
#             wR.buyUnitTimer.start()
#         except:
#             wR.buyUnitTimer = Timer(60, buyUnit)
#             wR.buyUnitTimer.start()
#             print 'Units not ready'
#         time.sleep(1)
#         pyautogui.click(706, 992)#Back to quests
#         print 'Finsihed buying Units'
#     else:
#         buyUnitTimer = Timer(20, buyUnit)
#         buyUnitTimer.start()
#     wR.buyingUnits=False

# def upgradeUnit():
#     if(wR.exiting):
#         return
#     if(not wR.arenaBattling and not wR.buyingUnits and not wR.xSpeeding and not wR.reviving and not wR.questing):
#         wR.upgradingUnits = True
#         print 'Upgrading Units'
#         pyautogui.click(800, 1000)#Clicks Unit
#         for a in xrange(3):
#             for b in xrange(2):
#                 time.sleep(.1)
#                 for i in pyautogui.locateAllOnScreen('coin.png'):
#                     pyautogui.click(i[0], i[1], clicks=4, interval = .02)
#             time.sleep(2.5)
#             pyautogui.moveTo(920,730)
#             pyautogui.dragRel(0, -450, .7, button='left')
#             time.sleep(.5)
#         for c in xrange(4):
#             pyautogui.moveTo(920,550)
#             pyautogui.dragRel(0, 300, .7, button='left')
#         time.sleep(.5)
#         try:
#             x,y = pyautogui.locateCenterOnScreen('x.png')
#             pyautogui.click(x, y)#Back to quests
#         except:
#             pass
#         pyautogui.click(706, 992)#Back to quests
#         wR.upgradeUnitTimer = Timer(120, upgradeUnit)
#         wR.upgradeUnitTimer.start()
#         print 'Finished Upgrading Units'
#     else:
#         wR.upgradeUnitTimer = Timer(20, upgradeUnit)
#         wR.upgradeUnitTimer.start()
#     wR.upgradingUnits = False

# def upgradeInitialQuests():
#     for i in xrange(8):
#         pyautogui.mouseDown(920, 650, button='left')
#         pyautogui.moveRel(0, 400, .3)
#         pyautogui.mouseUp(920, 650, button='left')
#     time.sleep(1)
#     for i in xrange(30):
#         for x in pyautogui.locateAllOnScreen('coin.png'):
#             if x[1] > 550:
#                 pyautogui.click(x[0]+10, x[1]+10)
#         pyautogui.mouseDown(920, 650, button='left')
#         pyautogui.moveRel(0, -135, .3)
#         pyautogui.mouseUp(920, 650, button='left')
#         time.sleep(2)
#         try:
#             x,y = pyautogui.locateCenterOnScreen('unit_confirm.png')
#             pyautogui.click(x, y)
#         except:
#             pass
#     for i in xrange(23):
#         time.sleep(.1)
#         pyautogui.click(1144, 516)
#     try:
#         x,y = pyautogui.locateCenterOnScreen('unit_confirm.png')
#         pyautogui.click(x, y)
#     except:
#         pass
#     try:
#         x,y = pyautogui.locateCenterOnScreen('discover_omen_diamonds.png')
#     except:
#         try:
#             x,y = pyautogui.locateCenterOnScreen('dispatch_omen_diamonds.png')
#         except:
#             try:
#                 x,y = pyautogui.locateCenterOnScreen('archdragon_diamonds.png')
#             except:
#                 upgradeInitialQuests()

# def openChests():
#     if(wR.exiting):
#         return
#     time.sleep(.02)
#     if(not wR.buyingUnits and not wR.upgradingUnits and not wR.arenaBattling and not wR.xSpeeding and not wR.reviving and not wR.reviving):
#         pyautogui.click(950, 360)#Clicks for chests
#     try:
#         x,y = pyautogui.locateCenterOnScreen('view_ad.png')
#         pyautogui.click(x, y)
#         time.sleep(1)
#         pyautogui.click(947, 713)#Hits confirm button
#     except:
#         pass
#         #print 'No Ad'
#     wR.openChestsTimer = Timer(.05, openChests)
#     wR.openChestsTimer.start()

# def xSpeed():
#     if(wR.exiting):
#         return
#     if(not wR.buyingUnits and not wR.upgradingUnits and not wR.arenaBattling and not wR.reviving and not wR.questing):
#         wR.xSpeeding = True
#         pyautogui.click(1180, 984)#opens shop
#         time.sleep(1)
#         try:
#             x,y = pyautogui.locateCenterOnScreen('view_ad2.png')
#             pyautogui.click(x, y)
#             time.sleep(3)
#             x,y = pyautogui.locateCenterOnScreen('shop_confirm.png')
#             pyautogui.click(x, y)
#             time.sleep(1)
#             wR.xSpeedTimer = Timer(5*60, xSpeed)
#             wR.xSpeedTimer.start()
#         except:
#             wR.xSpeedTimer = Timer(60, xSpeed)
#             wR.xSpeedTimer.start()
#         pyautogui.click(706, 992)#Back to quests
#         wR.xSpeeding = False
#     else:
#         wR.xSpeedTimer = Timer(60, xSpeed)
#         wR.xSpeedTimer.start()

# def autoQuest():
#     if wR.exiting:
#         return
#     if(not wR.buyingUnits and not wR.upgradingUnits and not wR.arenaBattling and not wR.xSpeeding and not wR.reviving and not wR.reviving):
#         wR.questing = True
#         pyautogui.click(706, 992)#Back to quests
#         for x in xrange(2):
#             time.sleep(.2)
#             for i in pyautogui.locateAllOnScreen('coin.png'):
#                 pyautogui.click(i[0]+10, i[1]+10, clicks=4, interval = .02)
#         try:
#             x,y = pyautogui.locateCenterOnScreen('auto_quest_confirm.png')
#             pyautogui.click(x, y)
#         except:
#             pass
#         time.sleep(.5)
#         wR.questing = False
#     wR.autoQuestTimer = Timer(25, autoQuest)
#     wR.autoQuestTimer.start()
#

# def autoRevive():
#     if(wR.exiting):
#         return
#     if(not wR.buyingUnits and not wR.upgradingUnits and not wR.arenaBattling and not wR.xSpeeding and not wR.questing):
#         wR.reviving = True
#         try:
#             level = ImageGrab.grab(bbox=(925,38,973,66))
#             text = int(image_to_string(level))
#             print 'Checking Level'
#             print 'You are at level', text
#             if text >= 4300:
#                 print 'Reviving at level', text
#                 pyautogui.click(800, 1000)#Clicks Unit
#                 time.sleep(1)
#                 x,y = pyautogui.locateCenterOnScreen('revive.png')
#                 print 1
#                 pyautogui.click(x, y)
#                 time.sleep(1)
#                 x,y = pyautogui.locateCenterOnScreen('revive.png')
#                 print 2
#                 pyautogui.click(x, y)
#                 time.sleep(1)
#                 x,y = pyautogui.locateCenterOnScreen('revival_team.png')
#                 print 3
#                 pyautogui.click(x, y)
#                 time.sleep(15)
#                 x,y = pyautogui.locateCenterOnScreen('battle_arena_confirm.png')
#                 print 4
#                 pyautogui.click(x, y)
#                 time.sleep(1)
#                 closeGame()
#                 openGame()
#                 upgradeInitialQuests()
#         except:
#             pass
#         wR.reviving = False
#     wR.autoReviveTimer = Timer(60, autoRevive)
#     wR.autoReviveTimer.start()

# autoRevive()
# openGame()
# upgradeInitialQuests()


"""MY FUNCS"""


def init():
    wR.level_check_time = time.time()
    wR.level_filter = [1] * 50
    wR.level = 1
    wR.check_number = 0
    wR.open_chests_counter = 0
    wR.max_quests_counter = 0
    wR.quests_add_rel = 0
    wR.distortion_passed = False
    wR.upgraded_units_once = False
    wR.max_level_reached = False


def revive(gems=False):
    if not wR.is_reopen_game:
        wR.is_revive = True
        w.stopTimer()
        time.sleep(wR.delay * 2 * 10)
        pyautogui.click(685, 145)
        time.sleep(wR.delay * 2 * 2)
        revival_done = False
        while not revival_done:
            try:
                if gems:
                    x, y = pyautogui.locateCenterOnScreen('ReviveGems.png', region=(700, 920, 300, 80))
                elif not gems:
                    x, y = pyautogui.locateCenterOnScreen('Revive.png', region=(1100, 940, 90, 50))
                pyautogui.click(x, y)
                time.sleep(wR.delay * 2 * 2)
                while not revival_done:
                    try:  # must
                        x, y = pyautogui.locateCenterOnScreen('ReviveasRevivalteam.png', region=(720, 675, 220, 50))
                        pyautogui.click(x, y)
                        time.sleep(wR.delay * 2 * 20)
                        # what if code?
                        try:
                            x, y = pyautogui.locateCenterOnScreen('SolveCode.png', region=(760, 150, 220, 100))
                            pyautogui.click(x, y)
                            time.sleep(wR.delay)
                            revival_done = True
                            counter = 0
                            while counter < 5:
                                try:
                                    send_gmail('EF update', ['max level reached!'], 'yechez18@gmail.com', 'Endless@wizard.com')
                                    counter = 5
                                except Exception as e:
                                    counter += 1
                                    time.sleep(wR.delay)
                            while True:
                                try:
                                    x, y = pyautogui.locateCenterOnScreen('CancelCode.png', region=(1050, 990, 100, 50))
                                    pyautogui.click(x, y)
                                    time.sleep(wR.delay)
                                    while True:
                                        try:
                                            x, y = pyautogui.locateCenterOnScreen('XRevive.png',
                                                                                  region=(1200, 45, 100, 100))
                                            pyautogui.click(x, y)
                                            time.sleep(wR.delay)
                                            break
                                        except:
                                            time.sleep(wR.delay)
                                    w.startTimer()
                                    wR.is_revive = False
                                    return
                                except:
                                    time.sleep(wR.delay)
                        except:
                            while not revival_done:
                                try:  # must
                                    x, y = pyautogui.locateCenterOnScreen('ConfirmRevive.png', region=(910, 950, 100, 50))
                                    pyautogui.click(x, y)
                                    time.sleep(wR.delay * 2 * 10)
                                    revival_done = True
                                    try:  # maybe
                                        x, y = pyautogui.locateCenterOnScreen('Join.png', region=(825, 660, 80, 50))
                                        pyautogui.click(x, y)
                                        time.sleep(wR.delay * 10 * 2)
                                        while True:
                                            try:  # maybe
                                                x, y = pyautogui.locateCenterOnScreen('JoinConfirm.png', region=(900, 650, 120, 50))
                                                pyautogui.click(x, y)
                                                time.sleep(wR.delay)
                                                break
                                            except Exception as e:
                                                time.sleep(wR.delay)
                                    except:
                                        time.sleep(wR.delay)
                                except:
                                    time.sleep(wR.delay)
                    except:
                        time.sleep(wR.delay)
            except:
                time.sleep(wR.delay)
        print('revived at level ', wR.level)
        init()
        w.startTimer()
        wR.is_revive = False


def reopen_game():
    wR.is_reopen_game = True
    w.stopTimer()
    time.sleep(wR.delay * 2 * 10)
    while True:
        try:
            x, y = pyautogui.locateCenterOnScreen('ServerConnectionLost.png', region=(900, 530, 120, 50))
            pyautogui.click(x, y)
            time.sleep(wR.delay * 2 * 10)
            break
        except:
            time.sleep(wR.delay)
    while True:
        try:
            x, y = pyautogui.locateCenterOnScreen('EndlessFrontier.png')
            pyautogui.click(x, y)
            time.sleep(wR.delay * 2 * 60)
            break
        except:
            time.sleep(wR.delay)
    while True:
        try:
            x, y = pyautogui.locateCenterOnScreen('fullScreen.png')
            pyautogui.click(x, y)
            time.sleep(wR.delay * 2 * 5)
            break
        except:
            time.sleep(wR.delay)
    while True:
        try:
            x, y = pyautogui.locateCenterOnScreen('startConfirm.png', region=(920, 880, 80, 50))
            pyautogui.click(x, y)
            time.sleep(wR.delay * 2 * 5)
            break
        except:
            time.sleep(wR.delay)
    while True:
        try:
            x, y = pyautogui.locateCenterOnScreen('XNews.png', region=(1150, 840, 50, 50))
            pyautogui.click(x, y)
            time.sleep(wR.delay * 2 * 5)
            break
        except:
            time.sleep(wR.delay)
    init()
    w.startTimer()
    wR.is_reopen_game = False


def detect_level():
    pyautogui.screenshot('lvl.png', region=(932, 43, 60, 23))
    im = Image.open("lvl.png")  # the second one
    im = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
    enhancer = ImageEnhance.Contrast(im)
    im = im.filter(ImageFilter.MinFilter(size=1))
    im = enhancer.enhance(3)
    im = im.convert('L')
    im.save('lvl.png')
    text = int(image_to_string(Image.open('lvl.png'), lang='eng', boxes=False, config='--psm 8 tessedit_char_whitelist 0123456789'))
    print(text)
    return text


def level_check():
    if not wR.max_level_reached:
        text = detect_level()
        wR.level_filter.insert(0, text)
        wR.level_filter.pop()
        filtered_level = statistics.median(wR.level_filter)

        if time.time() - wR.level_check_time >= 24:
            if filtered_level - wR.level < 10:
                if wR.level > 20800:
                    wR.max_level_reached = True
            wR.level = filtered_level
            wR.level_check_time = time.time()

        if wR.max_level_reached:
            revive()


def use_skills():
    try:
        level_check()
    except ValueError:
        pass
    if wR.exiting:
        return
    elif not wR.is_max_quests and not wR.is_upgrade_units and not wR.is_buy_units and not wR.is_revive and not wR.is_reopen_game:
        pyautogui.click(875, 85)
        pyautogui.click(935, 85)
        pyautogui.click(995, 85)
    wR.skills_timer = Timer(3, use_skills)
    wR.skills_timer.start()


def open_chests():
    if wR.exiting:
        return
    elif not wR.is_max_quests and not wR.is_upgrade_units and not wR.is_buy_units and not wR.is_revive and not wR.is_reopen_game:
        pyautogui.click(1000, 360)
        pyautogui.click(920, 360)
        pyautogui.click(850, 360)
        time.sleep(wR.delay_small / 2)
        if wR.open_chests_counter % 5 == 0:
            try:
                wR.is_open_chests = True
                x, y = pyautogui.locateCenterOnScreen('ViewAd.png', region=(795, 645, 150, 100))
                pyautogui.click(x, y)
                time.sleep(wR.delay)
                # try:
                #     x, y = pyautogui.locateCenterOnScreen('ViewAdConfirm.png')
                #     pyautogui.click(x, y)
                #     time.sleep(wR.delay)
                # except:
                #     pass
            except:
                if wR.check_number == 0:
                    try:
                        x, y = pyautogui.locateCenterOnScreen('distortion_confirm.png', region=(895, 810, 150, 100))
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                    except:
                        pass
                elif wR.check_number == 1:
                    try:
                        x, y = pyautogui.locateCenterOnScreen('quest_confirm.png', region=(875, 800, 150, 100))
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                    except:
                        pass
                elif wR.check_number == 2:
                    try:
                        x, y = pyautogui.locateCenterOnScreen('X_UpgradeAll.png', region=(1175, 175, 100, 100))
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                    except:
                        pass
                elif wR.check_number == 3:
                    try:
                        x, y = pyautogui.locateCenterOnScreen('X_UnitInfo.png', region=(1200, 90, 100, 100))
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                    except:
                        pass
                elif wR.check_number == 4:
                    try:
                        x, y = pyautogui.locateCenterOnScreen('Join.png', region=(825, 660, 80, 50))
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                    except:
                        pass
                elif wR.check_number == 5:
                    try:
                        x, y = pyautogui.locateCenterOnScreen('Distortion2Confirm.png', region=(900, 970, 120, 70))
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                    except:
                        pass
                elif wR.check_number == 6:
                    try:
                        x, y = pyautogui.locateCenterOnScreen('XAirships.png', region=(650, 40, 70, 70))
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                    except:
                        pass
                elif wR.check_number == 7:
                    try:
                        x, y = pyautogui.locateCenterOnScreen('XBuyUnitGems.png', region=(1185, 535, 70, 70))
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                    except:
                        pass
                elif wR.check_number == 8:
                    try:
                        x, y = pyautogui.locateCenterOnScreen('CancelRefresh.png', region=(1030, 700, 100, 50))
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                    except:
                        pass
                elif wR.check_number == 9:
                    try:
                        x, y = pyautogui.locateCenterOnScreen('ServerConnectionLost.png', region=(900, 530, 120, 50))
                        reopen_game()
                    except:
                        pass
                # elif wR.check_number == 4:
                #     try:
                #         x, y = pyautogui.locateCenterOnScreen('ViewAdConfirm.png')
                #         pyautogui.click(x, y)
                #         time.sleep(wR.delay)
                #     except:
                #         pass
                wR.check_number += 1
            finally:
                if wR.open_chests_counter >= 2000:
                    wR.open_chests_counter = 0
                if wR.check_number >= 10:
                    wR.check_number = 0

        wR.open_chests_counter += 1
        wR.is_open_chests = False

    wR.open_chests_timer = Timer(.02, open_chests)
    wR.open_chests_timer.start()


def max_quests():
    if wR.exiting:
        return
    elif not wR.is_upgrade_units and not wR.is_buy_units and not wR.is_revive and not wR.is_reopen_game:
        wR.is_max_quests = True
        drag_by = 102
        try:
            x, y = pyautogui.locateCenterOnScreen('quests.png', region=(660, 930, 100, 100))
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except:
            pass
        finally:
            if pyautogui.locateCenterOnScreen('questsOn.png', region=(660, 930, 100, 100)):
                for x in range(0, 5):
                    pyautogui.click(1180, 692 + wR.quests_add_rel)
                    pyautogui.click(1180, 692 - 40 + wR.quests_add_rel)
                    time.sleep(wR.delay_small)
                pyautogui.click(820, 692 + wR.quests_add_rel)
                pyautogui.click(820, 692 - 40 + wR.quests_add_rel)
                pyautogui.click(820, 692 + wR.quests_add_rel)
                pyautogui.click(820, 692 - 40 + wR.quests_add_rel)
                pyautogui.click(820, 692 + wR.quests_add_rel)
                pyautogui.click(820, 692 - 40 + wR.quests_add_rel)
                time.sleep(wR.delay_small)
                pyautogui.click(1180, 692 + wR.quests_add_rel)
                pyautogui.click(1180, 692 - 40 + wR.quests_add_rel)
                time.sleep(wR.delay)
                try:
                    x, y = pyautogui.locateCenterOnScreen('quest_confirm.png', region=(875, 800, 150, 100))
                    if pyautogui.locateCenterOnScreen('last_quest.png', region=(675, 545, 300, 120)):
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                        wR.is_max_quests = False
                        return
                    # elif pyautogui.locateCenterOnScreen('last_drag.png', region=(675, 545, 300, 120)):
                    #     wR.quests_add_rel += drag_by
                    #     pyautogui.click(x, y)
                    #     time.sleep(wR.delay)
                    else:
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                        pyautogui.dragRel(0, -drag_by, 1, tween=pyautogui.easeOutQuad, button='left')
                    wR.max_quests_counter = 0
                except:
                    wR.max_quests_counter += 1
                if wR.max_quests_counter > 10:
                    pyautogui.dragRel(0, drag_by, 1, tween=pyautogui.easeOutQuad, button='left')
        wR.is_max_quests = False

    wR.max_quests_timer = Timer(8, max_quests)
    wR.max_quests_timer.start()


def upgrade_units():
    if wR.exiting:
        return
    elif not wR.is_buy_units and not wR.is_max_quests and not wR.is_revive and not wR.is_reopen_game:
        wR.is_upgrade_units = True
        try:
            x, y = pyautogui.locateCenterOnScreen('Unit.png', region=(750, 935, 120, 100))
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except:
            try:
                x, y = pyautogui.locateCenterOnScreen('quests.png', region=(645, 930, 120, 100))
                pyautogui.click(x, y)
                time.sleep(wR.delay)
                x, y = pyautogui.locateCenterOnScreen('Unit.png', region=(750, 935, 120, 100))
                pyautogui.click(x, y)
                time.sleep(wR.delay)
            except:
                pass
        finally:
            if pyautogui.locateCenterOnScreen('UnitOn.png', region=(750, 935, 120, 100)):
                if not wR.upgraded_units_once:
                    try:
                        x, y = pyautogui.locateCenterOnScreen('UpgradeAll.png', region=(830, 510, 150, 100))
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                        for x in range(4):
                            pyautogui.click(745 + 143 * x, 410, clicks=5, interval=wR.delay_small)
                        time.sleep(wR.delay)
                        x, y = pyautogui.locateCenterOnScreen('X_UpgradeAll.png', region=(1175, 175, 100, 100))
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                        wR.upgraded_units_once = True
                    except:
                        pass
                else:
                    pyautogui.click(1180, 645, clicks=5, interval=wR.delay_small)
                    pyautogui.click(825, 645, clicks=5, interval=wR.delay_small)
                    pyautogui.click(1025, 645, clicks=5, interval=wR.delay_small)
                    time.sleep(wR.delay)
                    try:
                        x, y = pyautogui.locateCenterOnScreen('X_UnitInfo.png', region=(1200, 90, 100, 100))
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                    except:
                        pass
                wR.is_upgrade_units = False
    else:
        wR.upgrade_units_timer = Timer(30, upgrade_units)
        wR.upgrade_units_timer.start()
        return

    wR.upgrade_units_timer = Timer(3 * 60, upgrade_units)
    wR.upgrade_units_timer.start()


def buy_units():
    if wR.exiting:
        return
    elif not wR.is_upgrade_units and not wR.is_max_quests and not wR.is_revive and not wR.is_reopen_game:
        wR.is_buy_units = True
        time.sleep(wR.delay * 4)
        try:
            x, y = pyautogui.locateCenterOnScreen('Unit.png', region=(750, 935, 120, 100))
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except:
            try:
                x, y = pyautogui.locateCenterOnScreen('quests.png', region=(645, 930, 120, 100))
                pyautogui.click(x, y)
                time.sleep(wR.delay)
                x, y = pyautogui.locateCenterOnScreen('Unit.png', region=(750, 935, 120, 100))
                pyautogui.click(x, y)
                time.sleep(wR.delay)
            except:
                pass
        finally:
            try:
                x, y = pyautogui.locateCenterOnScreen('BuyUnit.png', region=(1110, 510, 150, 100))
                pyautogui.click(x, y)
                time.sleep(wR.delay)
                try:
                    x, y = pyautogui.locateCenterOnScreen('Refresh.png', region=(935, 510, 280, 100))
                    time.sleep(wR.delay * 2)
                    pyautogui.click(x, y)
                    time.sleep(wR.delay)
                    done = False
                    while not done:
                        try:
                            x, y = pyautogui.locateCenterOnScreen('BuyAll.png', region=(935, 510, 280, 100))
                            pyautogui.click(x, y)
                            time.sleep(wR.delay)
                            while not done:
                                try:
                                    x, y = pyautogui.locateCenterOnScreen('BuyAllConfirm.png',
                                                                          region=(800, 590, 150, 100))
                                    pyautogui.click(x, y)
                                    time.sleep(wR.delay)
                                    while not done:
                                        try:
                                            x, y = pyautogui.locateCenterOnScreen('BuyAllConfirm2.png',
                                                                                  region=(890, 620, 150, 100))
                                            pyautogui.click(x, y)
                                            time.sleep(wR.delay*2)
                                            done = True
                                        except:
                                            try:
                                                x, y = pyautogui.locateCenterOnScreen('BuyAllConfirm3.png',
                                                                                      region=(910, 660, 100, 40))
                                                pyautogui.click(x, y)
                                                time.sleep(wR.delay)
                                                done = True
                                            except:
                                                time.sleep(wR.delay)
                                except:
                                    time.sleep(wR.delay)
                        except:
                            try:
                                x, y = pyautogui.locateCenterOnScreen('UnitsRefreshingConfirm.png',
                                                                      region=(865, 690, 200, 100))
                                pyautogui.click(x, y)
                                time.sleep(wR.delay)
                            except:
                                time.sleep(wR.delay)
                except:
                    time.sleep(wR.delay)
            except:
                time.sleep(wR.delay)
        time.sleep(wR.delay * 4)
        wR.is_buy_units = False
    else:
        wR.buy_units_timer = Timer(30, buy_units)
        wR.buy_units_timer.start()
        return

    wR.buy_units_timer = Timer(6 * 60, buy_units)
    wR.buy_units_timer.start()


def upgrade_units():
    if wR.exiting:
        return
    elif not wR.is_buy_units and not wR.is_max_quests and not wR.is_revive and not wR.is_reopen_game:
        wR.is_upgrade_units = True
        try:
            x, y = pyautogui.locateCenterOnScreen('Unit.png', region=(750, 935, 120, 100))
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except:
            try:
                x, y = pyautogui.locateCenterOnScreen('quests.png', region=(645, 930, 120, 100))
                pyautogui.click(x, y)
                time.sleep(wR.delay)
                x, y = pyautogui.locateCenterOnScreen('Unit.png', region=(750, 935, 120, 100))
                pyautogui.click(x, y)
                time.sleep(wR.delay)
            except:
                pass
        finally:
            if pyautogui.locateCenterOnScreen('UnitOn.png', region=(750, 935, 120, 100)):
                if not wR.upgraded_units_once:
                    try:
                        x, y = pyautogui.locateCenterOnScreen('UpgradeAll.png', region=(830, 510, 150, 100))
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                        for x in range(4):
                            pyautogui.click(745 + 143 * x, 410, clicks=5, interval=wR.delay_small)
                        time.sleep(wR.delay)
                        x, y = pyautogui.locateCenterOnScreen('X_UpgradeAll.png', region=(1175, 175, 100, 100))
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                        wR.upgraded_units_once = True
                    except:
                        pass
                else:
                    pyautogui.click(1180, 645, clicks=5, interval=wR.delay_small)
                    pyautogui.click(825, 645, clicks=5, interval=wR.delay_small)
                    pyautogui.click(1025, 645, clicks=5, interval=wR.delay_small)
                    time.sleep(wR.delay)
                    try:
                        x, y = pyautogui.locateCenterOnScreen('X_UnitInfo.png', region=(1200, 90, 100, 100))
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                    except:
                        pass
                wR.is_upgrade_units = False
    else:
        wR.upgrade_units_timer = Timer(30, upgrade_units)
        wR.upgrade_units_timer.start()
        return

    wR.upgrade_units_timer = Timer(3 * 60, upgrade_units)
    wR.upgrade_units_timer.start()


"""Helpful functions"""

w = wR()
time.sleep(5)
w.startTimer()


def on_press(key):
    if key.char == 'p':
        wR.exiting = not wR.exiting
        if wR.exiting:
            w.stopTimer()
            print('Pausing')
        else:
            print('UnPausing')
            w.startTimer()
    elif key.char == 'e':
        print('Exiting')
        # stopTimer()
        wR.exiting = True
        sys.exit()
    else:
        pass


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
