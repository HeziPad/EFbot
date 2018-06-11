import statistics
import sys
import time
from threading import Timer

import pyautogui
import pytesseract
from pynput import keyboard

from imageProcessing import detect_level
from myemail import send_gmail

import logging

logging.basicConfig(filename='log.txt',
                    level=logging.DEBUG,
                    format='[ %(asctime)s ] [%(filename)20s:%(lineno)s - %(funcName)20s() ] [ %(levelname)7s ]%(message)s',
                    filemode='w')
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'


class wR():
    logging.info('creating a class member')
    is_use_skills = False
    is_reopen_game = False
    is_revive = False
    is_open_chests = False
    is_max_quests = False
    is_buy_units = False
    is_upgrade_units = False
    exiting = False
    spirit_rest = False
    delay = 0.5
    delay_small = 0.1

    start_time = time.time()
    level_check_time = time.time()
    level_filter = [1] * 20
    level = 1
    level_tmp = 1
    check_number = 0
    open_chests_counter = 0
    max_quests_counter = 0
    quests_add_rel = 0
    distortion_passed = False
    upgraded_units_once = False
    max_level_reached = False
    last_drag_reached = False

    def startTimer(self):
        logging.info('START timer')
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
        logging.info('START timer - done')

    def stopTimer(self):
        logging.info('STOP timer')
        self.skills_timer.cancel()
        self.open_chests_timer.cancel()
        self.max_quests_timer.cancel()
        self.upgrade_units_timer.cancel()
        self.buy_units_timer.cancel()
        logging.info('STOP timer - done')

    def startTimerSRmode(self):
        logging.info('START timer SR mode')
        self.buy_units_timer = Timer(2 * 60, buy_units)
        self.buy_units_timer.start()
        logging.info('START timer SR mode - done')

    def stopTimerSRmode(self):
        logging.info('STOP timer SR mode')
        self.buy_units_timer.cancel()
        logging.info('STOP timer SR mode - done')


"""MY FUNCS"""


def init():
    logging.info('init')
    wR.start_time = time.time()
    wR.level_check_time = time.time()
    wR.level_filter = [1] * 20
    wR.level = 1
    wR.level_tmp = 1
    wR.check_number = 0
    wR.open_chests_counter = 0
    wR.max_quests_counter = 0
    wR.quests_add_rel = 0
    wR.distortion_passed = False
    wR.upgraded_units_once = False
    wR.max_level_reached = False
    wR.last_drag_reached = False
    logging.info('init - done')


def revive(gems=False):
    logging.info('revive')
    if not wR.is_reopen_game and not wR.is_revive:
        wR.is_revive = True
        w.stopTimer()
        time.sleep(wR.delay * 2 * 10)
        pyautogui.click(685, 145)
        time.sleep(wR.delay * 2 * 2)
        revival_done = False
        while not revival_done:
            try:
                if gems:
                    logging.info('ReviveGems...')
                    x, y = pyautogui.locateCenterOnScreen('ReviveGems.png', region=(700, 920, 300, 80))
                    logging.info('ReviveGems found')
                elif not gems:
                    logging.info('Revive...')
                    x, y = pyautogui.locateCenterOnScreen('Revive.png', region=(1100, 940, 90, 50))
                    logging.info('Revive found')
                pyautogui.click(x, y)
                time.sleep(wR.delay * 2 * 2)
                while not revival_done:
                    try:  # must
                        logging.info('ReviveasRevivalteam...')
                        x, y = pyautogui.locateCenterOnScreen('ReviveasRevivalteam.png', region=(720, 675, 220, 50))
                        logging.info('ReviveasRevivalteam found')
                        pyautogui.click(x, y)
                        time.sleep(wR.delay*2*5)
                        # what if code?
                        try:
                            logging.info('SolveCode...')
                            x, y = pyautogui.locateCenterOnScreen('SolveCode.png', region=(760, 150, 220, 100))
                            logging.info('SolveCode found')
                            time.sleep(wR.delay)
                            revival_done = True
                            counter = 0
                            while counter < 5:
                                try:
                                    logging.info('Sending mail...')
                                    send_gmail('EF update', ['max level reached!'], 'yechez18@gmail.com', 'Endless@wizard.com')
                                    logging.info('Sending mail - done...')
                                    counter = 5
                                except Exception as e:
                                    logging.debug('Sending mail failed {}'.format(counter))
                                    counter += 1
                                    time.sleep(wR.delay)
                            while True:
                                try:
                                    logging.info('CancelCode...')
                                    x, y = pyautogui.locateCenterOnScreen('CancelCode.png', region=(1050, 990, 100, 50))
                                    logging.info('CancelCode found')
                                    pyautogui.click(x, y)
                                    time.sleep(wR.delay)
                                    while True:
                                        try:
                                            logging.info('XRevive...')
                                            x, y = pyautogui.locateCenterOnScreen('XRevive.png',
                                                                                  region=(1200, 45, 100, 100))
                                            logging.info('XRevive found')
                                            pyautogui.click(x, y)
                                            time.sleep(wR.delay)
                                            break
                                        except Exception as e:
                                            logging.error('XRevive NOT found {}'.format(e))
                                            time.sleep(wR.delay)
                                    w.startTimer()
                                    wR.is_revive = False
                                    logging.info('revive - done')
                                    return
                                except Exception as e:
                                    logging.error('CancelCode NOT found {}'.format(e))
                                    time.sleep(wR.delay)
                        except Exception as e:
                            logging.debug('SolveCode NOT found {}'.format(e))
                            while not revival_done:
                                try:  # must
                                    logging.info('ConfirmRevive...')
                                    x, y = pyautogui.locateCenterOnScreen('ConfirmRevive.png', region=(910, 950, 100, 50))
                                    time.sleep(wR.delay * 2 * 5)
                                    logging.info('ConfirmRevive found')
                                    pyautogui.click(x, y)
                                    time.sleep(wR.delay * 2 * 20)
                                    revival_done = True
                                    try:  # maybe
                                        logging.info('Join...')
                                        x, y = pyautogui.locateCenterOnScreen('Join.png', region=(825, 660, 80, 50))
                                        logging.info('Join found')
                                        pyautogui.click(x, y)
                                        time.sleep(wR.delay * 10 * 2)
                                        while True:
                                            try:  # maybe
                                                logging.info('JoinConfirm...')
                                                x, y = pyautogui.locateCenterOnScreen('JoinConfirm.png', region=(900, 650, 120, 50))
                                                logging.info('JoinConfirm found')
                                                pyautogui.click(x, y)
                                                time.sleep(wR.delay)
                                                break
                                            except Exception as e:
                                                logging.error('JoinConfirm NOT found {}'.format(e))
                                                time.sleep(wR.delay)
                                    except Exception as e:
                                        logging.debug('Join NOT found {}'.format(e))
                                        time.sleep(wR.delay)
                                except Exception as e:
                                    logging.error('ConfirmRevive NOT found {}'.format(e))
                                    time.sleep(wR.delay)
                    except Exception as e:
                        logging.error('ReviveasRevivalteam NOT found {}'.format(e))
                        time.sleep(wR.delay)
            except Exception as e:
                logging.error('ReviveGems / Revive NOT found {}'.format(e))
                time.sleep(wR.delay)
        logging.info('revived at level {} in {} seconds'.format(wR.level, (time.time() - wR.start_time)/60.0))
        print('revived at level {} in {} seconds'.format(wR.level, (time.time() - wR.start_time)/60.0))
        init()
        w.startTimer()
        wR.is_revive = False
    logging.info('revive - done')


def reopen_game():
    logging.info('reopen_game')
    wR.is_reopen_game = True
    w.stopTimer()
    time.sleep(wR.delay * 2 * 10)
    while True:
        try:
            logging.info('ServerConnectionLost...')
            x, y = pyautogui.locateCenterOnScreen('ServerConnectionLost.png', region=(900, 530, 120, 50))
            logging.info('ServerConnectionLost found')
            pyautogui.click(x, y)
            time.sleep(wR.delay * 2 * 10)
            break
        except Exception as e:
            logging.error('ServerConnectionLost NOT found {}'.format(e))
            time.sleep(wR.delay)
    while True:
        try:
            logging.info('EndlessFrontier...')
            x, y = pyautogui.locateCenterOnScreen('EndlessFrontier.png')
            logging.info('EndlessFrontier found')
            pyautogui.click(x, y)
            time.sleep(wR.delay * 2 * 60)
            break
        except Exception as e:
            logging.error('EndlessFrontier NOT found {}'.format(e))
            time.sleep(wR.delay)
    while True:
        try:
            logging.info('fullScreen...')
            x, y = pyautogui.locateCenterOnScreen('fullScreen.png')
            logging.info('fullScreen found')
            pyautogui.click(x, y)
            time.sleep(wR.delay * 2 * 5)
            break
        except Exception as e:
            logging.error('fullScreen NOT found {}'.format(e))
            time.sleep(wR.delay)
    while True:
        try:
            logging.info('startConfirm...')
            x, y = pyautogui.locateCenterOnScreen('startConfirm.png', region=(920, 880, 80, 50))
            logging.info('startConfirm found {}'.format(e))
            pyautogui.click(x, y)
            time.sleep(wR.delay * 2 * 5)
            break
        except Exception as e:
            logging.error('startConfirm NOT found {}'.format(e))
            time.sleep(wR.delay)
    while True:
        try:
            logging.info('XNews...')
            x, y = pyautogui.locateCenterOnScreen('XNews.png', region=(1150, 840, 50, 50))
            logging.info('XNews found')
            pyautogui.click(x, y)
            time.sleep(wR.delay * 2 * 5)
            break
        except Exception as e:
            logging.error('XNews NOT found {}'.format(e))
            time.sleep(wR.delay)
    init()
    w.startTimer()
    wR.is_reopen_game = False
    logging.info('reopen_game - done')


def level_check():
    logging.info('level_check')
    if not wR.max_level_reached:
        try:
            text = detect_level()
            logging.debug('detected level = {}'.format(text))
            if 25000 >= text >= statistics.median(wR.level_filter):
                wR.level_filter.insert(0, text)
                wR.level_filter.pop()
        except ValueError as e:
            wR.level_filter.insert(0, wR.level_filter[0])
            wR.level_filter.pop()
            logging.debug('wR.level_filter = {}'.format(wR.level_filter))
        finally:
            filtered_level = statistics.median(wR.level_filter)
            logging.debug('filtered_level = {} wR.level_filter = {}'.format(filtered_level, wR.level_filter))

            logging.debug('filtered_level > wR.level ?')
            if filtered_level > wR.level:
                wR.level = filtered_level
                logging.debug('Yes. wR.level = {}'.format(wR.level))
            else:
                logging.debug('No.')
            logging.info('level_check - done')

            logging.debug('time.time() - wR.level_check_time >= 60 ?')
            if time.time() - wR.level_check_time >= 90:
                logging.debug('Yes. wR.level - wR.level_tmp < 10 ?')
                if wR.level - wR.level_tmp < 10:
                    logging.debug('Yes. wR.level > 20800 ?')
                    if wR.level > 21800:
                        wR.max_level_reached = True
                        logging.debug('Yes. wR.max_level_reached = {}'.format(wR.max_level_reached))
                    else:
                        logging.debug('No.')
                else:
                    logging.debug('No.')
                    wR.level_tmp = wR.level
                    wR.level_check_time = time.time()
            else:
                logging.debug('No.')
                logging.debug('wR.level_tmp = {} wR.level_check_time = {}'.format(wR.level, time.strftime('%H:%M:%S')))

            logging.debug('wR.max_level_reached ?')
            if wR.max_level_reached:
                logging.debug('Yes.')
                revive()
            else:
                logging.debug('No')


def use_skills():
    logging.info('use_skills')
    level_check()
    if wR.exiting:
        return
    elif not wR.is_max_quests and not wR.is_upgrade_units and not wR.is_buy_units and not wR.is_revive and not wR.is_reopen_game and not wR.is_use_skills:
        wR.is_use_skills = True
        logging.info('clicking skills')
        pyautogui.click(875, 85)
        pyautogui.click(935, 85)
        pyautogui.click(995, 85)

    wR.is_use_skills = False
    logging.info('use_skills - done')
    wR.skills_timer = Timer(3, use_skills)
    wR.skills_timer.start()


def open_chests():
    logging.info('open_chests')
    if wR.exiting:
        return
    elif not wR.is_max_quests and not wR.is_upgrade_units and not wR.is_buy_units and not wR.is_revive and not wR.is_reopen_game and not wR.is_open_chests:
        wR.is_open_chests = True
        logging.info('clicking chests')
        pyautogui.click(1000, 360)
        pyautogui.click(920, 360)
        pyautogui.click(850, 360)
        time.sleep(wR.delay_small / 2)
        if wR.open_chests_counter % 5 == 0:
            try:
                logging.info('ViewAd...')
                x, y = pyautogui.locateCenterOnScreen('ViewAd.png', region=(795, 645, 150, 100))
                logging.info('ViewAd found')
                pyautogui.click(x, y)
                time.sleep(wR.delay)
                # try:
                #     x, y = pyautogui.locateCenterOnScreen('ViewAdConfirm.png')
                #     pyautogui.click(x, y)
                #     time.sleep(wR.delay)
                # except:
                #     pass
            except Exception as e:
                logging.debug('ViewAd NOT found {}'.format(e))
                if wR.check_number == 0:
                    try:
                        logging.info('distortion_confirm...')
                        x, y = pyautogui.locateCenterOnScreen('distortion_confirm.png', region=(895, 810, 150, 100))
                        logging.info('distortion_confirm found')
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                    except Exception as e:
                        logging.debug('distortion_confirm NOT found {}'.format(e))
                elif wR.check_number == 1:
                    try:
                        logging.info('quest_confirm...')
                        x, y = pyautogui.locateCenterOnScreen('quest_confirm.png', region=(875, 800, 150, 100))
                        logging.info('quest_confirm found')
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                    except Exception as e:
                        logging.debug('quest_confirm NOT found {}'.format(e))
                elif wR.check_number == 2:
                    try:
                        logging.info('X_UpgradeAll...')
                        x, y = pyautogui.locateCenterOnScreen('X_UpgradeAll.png', region=(1175, 175, 100, 100))
                        logging.info('X_UpgradeAll found')
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                    except Exception as e:
                        logging.debug('X_UpgradeAll NOT found {}'.format(e))
                elif wR.check_number == 3:
                    try:
                        logging.info('X_UnitInfo...')
                        x, y = pyautogui.locateCenterOnScreen('X_UnitInfo.png', region=(1200, 90, 100, 100))
                        logging.info('X_UnitInfo found')
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                    except Exception as e:
                        logging.debug('X_UnitInfo NOT found {}'.format(e))
                elif wR.check_number == 4:
                    try:
                        logging.info('Join...')
                        x, y = pyautogui.locateCenterOnScreen('Join.png', region=(825, 660, 80, 50))
                        logging.info('Join found')
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                    except Exception as e:
                        logging.debug('Join NOT found {}'.format(e))
                elif wR.check_number == 5:
                    try:
                        logging.info('Distortion2Confirm...')
                        x, y = pyautogui.locateCenterOnScreen('Distortion2Confirm.png', region=(900, 970, 120, 70))
                        logging.info('Distortion2Confirm found')
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                    except Exception as e:
                        logging.debug('Distortion2Confirm NOT found {}'.format(e))
                elif wR.check_number == 6:
                    try:
                        logging.info('XAirships...')
                        x, y = pyautogui.locateCenterOnScreen('XAirships.png', region=(650, 40, 70, 70))
                        logging.info('XAirships found')
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                    except Exception as e:
                        logging.debug('XAirships NOT found {}'.format(e))
                elif wR.check_number == 7:
                    try:
                        logging.info('XBuyUnitGems...')
                        x, y = pyautogui.locateCenterOnScreen('XBuyUnitGems.png', region=(1185, 535, 70, 70))
                        logging.info('XBuyUnitGems found')
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                    except Exception as e:
                        logging.debug('XBuyUnitGems NOT found {}'.format(e))
                elif wR.check_number == 8:
                    try:
                        logging.info('CancelRefresh...')
                        x, y = pyautogui.locateCenterOnScreen('CancelRefresh.png', region=(1030, 700, 100, 50))
                        logging.info('CancelRefresh found')
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                    except Exception as e:
                        logging.debug('CancelRefresh NOT found {}'.format(e))
                elif wR.check_number == 9:
                    try:
                        logging.info('ServerConnectionLost...')
                        if pyautogui.locateCenterOnScreen('ServerConnectionLost.png', region=(900, 530, 120, 50)):
                            logging.info('ServerConnectionLost found')
                            reopen_game()
                        else:
                            logging.debug('ServerConnectionLost NOT found {}'.format(e))
                    except Exception as e:
                        logging.debug('ServerConnectionLost NOT found {}'.format(e))
                elif wR.check_number == 10:
                    try:
                        logging.info('XBuyUnit...')
                        x, y = pyautogui.locateCenterOnScreen('XBuyUnit.png', region=(1200, 100, 65, 65))
                        logging.info('XBuyUnit found')
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                    except Exception as e:
                        logging.debug('XBuyUnit NOT found {}'.format(e))
                wR.check_number += 1
            finally:
                logging.debug('wR.open_chests_counter = {} wR.check_number = {}'.format(wR.open_chests_counter, wR.check_number))
                if wR.open_chests_counter >= 2000:
                    wR.open_chests_counter = 0
                if wR.check_number >= 11:
                    wR.check_number = 0

        wR.open_chests_counter += 1
        wR.is_open_chests = False

    wR.open_chests_timer = Timer(.1, open_chests)
    wR.open_chests_timer.start()
    logging.info('open_chests - done')


def max_quests():
    logging.info('max_quests')
    if wR.exiting:
        return
    elif not wR.is_upgrade_units and not wR.is_buy_units and not wR.is_revive and not wR.is_reopen_game and not wR.is_max_quests:
        wR.is_max_quests = True
        drag_by = 102
        try:
            logging.info('quests...')
            x, y = pyautogui.locateCenterOnScreen('quests.png', region=(660, 930, 100, 100))
            logging.info('quests found')
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except Exception as e:
            logging.debug('quests NOT found {}'.format(e))
        finally:
            if pyautogui.locateCenterOnScreen('questsOn.png', region=(660, 930, 100, 100)):
                logging.debug('wR.quests_add_rel = {}'.format(wR.quests_add_rel))
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
                    logging.info('quest_confirm...')
                    x, y = pyautogui.locateCenterOnScreen('quest_confirm.png', region=(875, 800, 150, 100))
                    logging.info('quest_confirm found')
                    if pyautogui.locateCenterOnScreen('last_quest.png', region=(675, 545, 300, 120)):
                        logging.info('last_quest found')
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                        wR.is_max_quests = False
                        logging.info('max_quests - done')
                        return
                    elif pyautogui.locateCenterOnScreen('last_drag.png', region=(675, 545, 300, 120)):
                        logging.info('last_drag found')
                        wR.last_drag_reached = True
                        wR.quests_add_rel += drag_by
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                        logging.debug('wR.last_drag_reached = {} wR.quests_add_rel = {}'.format(wR.last_drag_reached, wR.quests_add_rel))
                    else:
                        logging.info('last_quest/last_drag NOT found')
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                        pyautogui.dragRel(0, -drag_by, 1, tween=pyautogui.easeOutQuad, button='left')
                    wR.max_quests_counter = 0
                except Exception as e:
                    logging.debug('quest_confirm NOT found {}'.format(e))
                    wR.max_quests_counter += 1
                if wR.max_quests_counter > 6:
                    logging.debug('wR.max_quests_counter = {} wR.last_drag_reached = {}'.format(wR.max_quests_counter, wR.last_drag_reached))
                    if not wR.last_drag_reached:
                        pyautogui.dragRel(0, drag_by, 1, tween=pyautogui.easeOutQuad, button='left')
            else:
                logging.error('questsOn NOT found')
        wR.is_max_quests = False

    wR.max_quests_timer = Timer(2 + wR.max_quests_counter, max_quests)
    wR.max_quests_timer.start()
    logging.info('max_quests - done')


def buy_units():
    logging.info('buy_units')
    if wR.exiting:
        return
    elif not wR.is_upgrade_units and not wR.is_max_quests and not wR.is_revive and not wR.is_reopen_game and not wR.is_buy_units:
        wR.is_buy_units = True
        time.sleep(wR.delay * 4)
        try:
            logging.info('Unit...')
            x, y = pyautogui.locateCenterOnScreen('Unit.png', region=(750, 935, 120, 100))
            logging.info('Unit found')
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except Exception as e:
            logging.debug('Unit NOT found {}'.format(e))
            try:
                logging.info('quests...')
                x, y = pyautogui.locateCenterOnScreen('quests.png', region=(645, 930, 120, 100))
                logging.info('quests found')
                pyautogui.click(x, y)
                time.sleep(wR.delay)
                logging.info('Unit...')
                x, y = pyautogui.locateCenterOnScreen('Unit.png', region=(750, 935, 120, 100))
                logging.info('Unit found')
                pyautogui.click(x, y)
                time.sleep(wR.delay)
            except Exception as e:
                logging.debug('quests / Unit NOT found {}'.format(e))
        finally:
            try:
                logging.info('BuyUnit...')
                x, y = pyautogui.locateCenterOnScreen('BuyUnit.png', region=(1110, 510, 150, 100))
                logging.info('BuyUnit found')
                pyautogui.click(x, y)
                time.sleep(wR.delay)
                try:
                    logging.info('Refresh...')
                    x, y = pyautogui.locateCenterOnScreen('Refresh.png', region=(935, 510, 280, 100))
                    logging.info('Refresh found')
                    time.sleep(wR.delay * 2 * 2)
                    pyautogui.click(x, y)
                    time.sleep(wR.delay)
                    done = False
                    while not done:
                        try:
                            logging.info('BuyAll...')
                            x, y = pyautogui.locateCenterOnScreen('BuyAll.png', region=(935, 510, 280, 100))
                            logging.info('BuyAll found')
                            pyautogui.click(x, y)
                            time.sleep(wR.delay)
                            while not done:
                                try:
                                    logging.info('BuyAllConfirm...')
                                    x, y = pyautogui.locateCenterOnScreen('BuyAllConfirm.png',
                                                                          region=(800, 590, 150, 100))
                                    logging.info('BuyAllConfirm found')
                                    pyautogui.click(x, y)
                                    time.sleep(wR.delay)
                                    while not done:
                                        try:
                                            logging.info('BuyAllConfirm2...')
                                            x, y = pyautogui.locateCenterOnScreen('BuyAllConfirm2.png',
                                                                                  region=(890, 620, 150, 100))
                                            logging.info('BuyAllConfirm2 found')
                                            pyautogui.click(x, y)
                                            time.sleep(wR.delay*2)
                                            done = True
                                        except Exception as e:
                                            logging.debug('BuyAllConfirm2 NOT found {}'.format(e))
                                            try:
                                                logging.info('BuyAllConfirm3...')
                                                x, y = pyautogui.locateCenterOnScreen('BuyAllConfirm3.png',
                                                                                      region=(910, 660, 100, 40))
                                                logging.info('BuyAllConfirm3 found')
                                                pyautogui.click(x, y)
                                                time.sleep(wR.delay)
                                                done = True
                                            except Exception as e:
                                                logging.debug('BuyAllConfirm3 NOT found {}'.format(e))
                                                time.sleep(wR.delay)
                                except Exception as e:
                                    logging.debug('BuyAllConfirm NOT found {}'.format(e))
                                    time.sleep(wR.delay)
                        except Exception as e:
                            logging.debug('BuyAll NOT found {}'.format(e))
                            try:
                                logging.info('UnitsRefreshingConfirm...')
                                x, y = pyautogui.locateCenterOnScreen('UnitsRefreshingConfirm.png',
                                                                      region=(865, 690, 200, 100))
                                logging.info('UnitsRefreshingConfirm found')
                                pyautogui.click(x, y)
                                time.sleep(wR.delay)
                            except Exception as e:
                                logging.debug('UnitsRefreshingConfirm NOT found {}'.format(e))
                                time.sleep(wR.delay)
                except Exception as e:
                    logging.debug('Refresh NOT found {}'.format(e))
                    time.sleep(wR.delay)
            except Exception as e:
                logging.debug('BuyUnit NOT found {}'.format(e))
                time.sleep(wR.delay)
        time.sleep(wR.delay * 4)
    else:
        wR.buy_units_timer = Timer(30, buy_units)
        wR.buy_units_timer.start()
        wR.is_buy_units = False
        logging.info('buy_units - done - reduced timer')
        return

    wR.is_buy_units = False
    logging.info('buy_units - done')
    wR.buy_units_timer = Timer(6 * 60, buy_units)
    wR.buy_units_timer.start()


def upgrade_units():
    logging.info('upgrade_units')
    if wR.exiting:
        return
    elif not wR.is_buy_units and not wR.is_max_quests and not wR.is_revive and not wR.is_reopen_game and not wR.is_upgrade_units:
        wR.is_upgrade_units = True
        try:
            logging.info('Unit...')
            x, y = pyautogui.locateCenterOnScreen('Unit.png', region=(750, 935, 120, 100))
            logging.info('Unit found')
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except Exception as e:
            logging.debug('Unit NOT found {}'.format(e))
            try:
                logging.info('quests...')
                x, y = pyautogui.locateCenterOnScreen('quests.png', region=(645, 930, 120, 100))
                logging.info('quests found')
                pyautogui.click(x, y)
                time.sleep(wR.delay)
                logging.info('Unit...')
                x, y = pyautogui.locateCenterOnScreen('Unit.png', region=(750, 935, 120, 100))
                logging.info('Unit found')
                pyautogui.click(x, y)
                time.sleep(wR.delay)
            except Exception as e:
                logging.debug('Unit/quests NOT found {}'.format(e))
        finally:
            if pyautogui.locateCenterOnScreen('UnitOn.png', region=(750, 935, 120, 100)):
                logging.debug('wR.upgraded_units_once = {}'.format(wR.upgraded_units_once))
                if not wR.upgraded_units_once:
                    try:
                        logging.info('UpgradeAll...')
                        x, y = pyautogui.locateCenterOnScreen('UpgradeAll.png', region=(830, 510, 150, 100))
                        logging.info('UpgradeAll found')
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                        for x in range(4):
                            pyautogui.click(745 + 143 * x, 410, clicks=5, interval=wR.delay_small)
                        time.sleep(wR.delay)
                        logging.info('X_UpgradeAll...')
                        x, y = pyautogui.locateCenterOnScreen('X_UpgradeAll.png', region=(1175, 175, 100, 100))
                        logging.info('X_UpgradeAll found')
                        pyautogui.click(x, y)
                        time.sleep(wR.delay)
                        wR.upgraded_units_once = True
                    except Exception as e:
                        logging.debug('X_UpgradeAll NOT found {}'.format(e))
                else:
                    pyautogui.click(1180, 645, clicks=5, interval=wR.delay_small)
                    pyautogui.click(825, 645, clicks=5, interval=wR.delay_small)
                    pyautogui.click(1025, 645, clicks=5, interval=wR.delay_small)
                    time.sleep(wR.delay * 2 * 2)
                    try:
                        logging.info('X_UnitInfo...')
                        x, y = pyautogui.locateCenterOnScreen('X_UnitInfo.png', region=(1200, 90, 100, 100))
                        logging.info('X_UnitInfo found')
                        pyautogui.click(x, y)
                        time.sleep(wR.delay * 2 * 2)
                    except Exception as e:
                        logging.debug('X_UnitInfo NOT found {}'.format(e))
                    pyautogui.click(1180, 750, clicks=5, interval=wR.delay_small)
                    pyautogui.click(825, 750, clicks=5, interval=wR.delay_small)
                    pyautogui.click(1025, 750, clicks=5, interval=wR.delay_small)
                    time.sleep(wR.delay * 2 * 2)
                    try:
                        logging.info('X_UnitInfo...')
                        x, y = pyautogui.locateCenterOnScreen('X_UnitInfo.png', region=(1200, 90, 100, 100))
                        logging.info('X_UnitInfo found')
                        pyautogui.click(x, y)
                        time.sleep(wR.delay * 2 * 2)
                    except Exception as e:
                        logging.debug('X_UnitInfo NOT found {}'.format(e))
            else:
                logging.error('UnitOn NOT found')
    else:
        wR.upgrade_units_timer = Timer(30, upgrade_units)
        wR.upgrade_units_timer.start()
        wR.is_upgrade_units = False
        logging.info('upgrade_units - done for good')
        return

    wR.is_upgrade_units = False
    logging.info('upgrade_units - done')
    wR.upgrade_units_timer = Timer(6 * 60, upgrade_units)
    wR.upgrade_units_timer.start()


w = wR()
time.sleep(5)
w.startTimer()


def on_press(key):
    if key.char == 'p':
        wR.exiting = not wR.exiting
        if wR.exiting:
            w.stopTimer()
            print('Pausing')
            logging.info('Pausing')
        else:
            print('UnPausing')
            logging.info('UnPausing')
            w.startTimer()
    elif key.char == 'e':
        print('Exiting')
        logging.info('Exiting')
        wR.exiting = True
        sys.exit()
    elif key.char == 's':
        wR.spirit_rest = not wR.spirit_rest
        if wR.spirit_rest:
            print('Starting SR mode')
            logging.info('Starting SR mode')
            w.stopTimer()
            time.sleep(wR.delay * 2 * 10)
            w.startTimerSRmode()
        else:
            print('Stoping SR mode')
            logging.info('Stoping SR mode')
            w.stopTimerSRmode()
            time.sleep(wR.delay * 2 * 10)
            w.startTimer()
    else:
        logging.info('Another Key pressed')


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
