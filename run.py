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
    is_solve_code = False

    exiting = False  # Don't use
    spirit_rest = False  # Don't use
    gems = True
    use_power = True
    screen_saver_on = False
    delay = 0.5
    delay_small = 0.1
    max_revive = 38800
    min_revive = max_revive - 1000
    min_lvl_detect = 20000
    MAX_MIN_TO_REV = 90

    start_time = time.time()
    level_check_time = time.time()
    level_filter = [1] * 80
    filter = [1] * 10
    level = 1
    level_tmp = 1
    check_number = 0
    open_chests_counter = 0
    max_quests_counter = 0
    quests_add_rel = 0
    upgraded_units_once = False
    max_level_reached = False
    last_drag_reached = False
    power_used = False

    def startTimer(self):
        logging.info('START timer')
        self.skills_timer = Timer(2, use_skills)
        self.skills_timer.start()
        self.open_chests_timer = Timer(3, open_chests)
        self.open_chests_timer.start()
        self.max_quests_timer = Timer(4, max_quests)
        self.max_quests_timer.start()
        self.upgrade_units_timer = Timer(6 * 60, upgrade_units)
        self.upgrade_units_timer.start()
        self.buy_units_timer = Timer(10, buy_units)
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


def close_game():
    try:
        x, y = pyautogui.locateCenterOnScreen('./pictures/exit_game.png', region=(1860, 0, 59, 40))
        logging.info('exit_game.png found')
        pyautogui.click(x, y)
        time.sleep(wR.delay * 2 * 5)
        logging.info('SUCCESS')
        return 0
    except Exception as e:
        logging.debug('failed to close game')
        return 0


def open_game():
    logging.debug('opening game')
    vm = ["C:\Program Files\Leapdroid\VM\LeapdroidVM.exe", '-vfiber', '-s', 'vm1']
    subprocess.Popen(vm)


def init():
    logging.info('init')
    wR.start_time = time.time()
    wR.level_check_time = time.time()
    wR.level_filter = [1] * 80
    wR.filter = [1] * 10
    wR.level = 1
    wR.level_tmp = 1
    wR.check_number = 0
    wR.open_chests_counter = 0
    wR.max_quests_counter = 0
    wR.quests_add_rel = 0
    wR.power_used = False
    wR.upgraded_units_once = False
    wR.max_level_reached = False
    wR.last_drag_reached = False
    logging.info('init - done')


def revive():
    if not wR.is_reopen_game and not wR.is_revive and not wR.is_solve_code:
        wR.is_revive = True
        w.stopTimer()
        time.sleep(wR.delay * 2 * 10)
        revival_done = False
        while not revival_done:
            try:
                if not wR.power_used and wR.use_power:
                    power()
                    time.sleep(180)
                    wR.power_used = True

                time.sleep(wR.delay * 2 * 2)
                pyautogui.click(685, 145)
                time.sleep(wR.delay * 2 * 2)
                if wR.gems:
                    x, y = pyautogui.locateCenterOnScreen('./pictures/ReviveGems.png', region=(700, 920, 300, 80))
                    logging.info('ReviveGems found')
                elif not wR.gems:
                    x, y = pyautogui.locateCenterOnScreen('./pictures/Revive.png', region=(1100, 940, 90, 50))
                    logging.info('Revive found')
                pyautogui.click(x, y)
                time.sleep(wR.delay * 2 * 2)
                while not revival_done:
                    try:  # must
                        x, y = pyautogui.locateCenterOnScreen('./pictures/ReviveasRevivalteam.png', region=(720, 675, 220, 50))
                        logging.info('ReviveasRevivalteam found')
                        pyautogui.click(x, y)
                        time.sleep(wR.delay*2*5)
                        try:
                            x, y = pyautogui.locateCenterOnScreen('./pictures/SolveCode.png', region=(730, 80, 100, 50))
                            logging.info('SolveCode found')
                            try:
                                counter = 0
                                while counter < 5:
                                    try:
                                        if solve_code():
                                            revival_done = True
                                            counter = 5
                                        else:
                                            counter += 1
                                    except Exception as e:
                                        print('not so good',e)
                                        logging.debug('solve_code failed! {}'.format(e))
                                        counter += 1
                                if revival_done:
                                    print('SOLVED THE MADEFUCKA CODE!!!')
                                    revival_done = check_after_revive()
                                else:
                                    raise Exception('didnt solve code')
                            except Exception as e:
                                counter = 0
                                while counter < 5:
                                    try:
                                        logging.info('Sending mail...')
                                        send_gmail('EF update', ['max level reached!'], 'yechez18@gmail.com',
                                                   'Endless@wizard.com')
                                        logging.info('Sending mail - done...')
                                        counter = 5
                                    except Exception as e:
                                        logging.debug('Sending mail failed {}'.format(counter))
                                        counter += 1
                                        time.sleep(wR.delay)
                                while True:
                                    try:
                                        x, y = pyautogui.locateCenterOnScreen('./pictures/CancelCode.png')
                                                                              #, region=(1030, 955, 100, 100))
                                        logging.info('CancelCode found')
                                        pyautogui.click(x, y)
                                        time.sleep(wR.delay)
                                        while True:
                                            try:
                                                x, y = pyautogui.locateCenterOnScreen('./pictures/XRevive.png',
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
                            revival_done = check_after_revive()
                    except Exception as e:
                        logging.error('ReviveasRevivalteam NOT found {}'.format(e))
                        time.sleep(wR.delay)
            except Exception as e:
                logging.error('ReviveGems / Revive NOT found {}'.format(e))
                check_popups()
                time.sleep(wR.delay)
        logging.info('revived at level {} in {} minutes'.format(wR.level, (time.time() - wR.start_time)/60.0))
        print('revived at level {} in {} minutes'.format(statistics.median(wR.level_filter), (time.time() - wR.start_time)/60.0))
        init()
        w.startTimer()
        wR.is_revive = False
    logging.info('revive - done')


def power():
    pyautogui.click(1220, 980)
    time.sleep(wR.delay * 2)
    if pyautogui.locateCenterOnScreen('./pictures/shopOn.png', region=(1175, 940, 100, 100)):
        logging.info('shopOn found')
        pyautogui.click(970, 460)
        try:
            pyautogui.moveTo(930, 770)
            pyautogui.dragRel(0, 200, 1, tween=pyautogui.easeOutQuad, button='left')
            time.sleep(wR.delay * 2)
            pyautogui.click(1200, 765)
            time.sleep(wR.delay * 2)
            try:
                x, y = pyautogui.locateCenterOnScreen('./pictures/powerConfirm.png', region=(800, 775, 100, 70))
                logging.info('powerConfirm found')
                pyautogui.click(x, y)
                time.sleep(wR.delay)
                wR.power_used = True
            except Exception as e:
                logging.debug('powerConfirm NOT found {}'.format(e))
        except Exception as e:
            logging.debug('ViewAd NOT found {}'.format(e))


def check_popups(check_number=None):
    try:
        x, y = pyautogui.locateCenterOnScreen('./pictures/ViewAd.png', region=(795, 645, 150, 100))
        logging.info('ViewAd found')
        pyautogui.click(x, y)
        time.sleep(wR.delay)
    except Exception as e:
        logging.debug('ViewAd NOT found {}'.format(e))

    if check_number == 0 or check_number is None:
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/distortion_confirm.png', region=(895, 810, 150, 100))
            logging.info('distortion_confirm found')
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except Exception as e:
            logging.debug('distortion_confirm NOT found {}'.format(e))
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/quest_confirm.png', region=(875, 800, 150, 100))
            logging.info('quest_confirm found')
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except Exception as e:
            logging.debug('quest_confirm NOT found {}'.format(e))
    if check_number == 1 or check_number is None:
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/X_UpgradeAll.png', region=(1175, 175, 100, 100))
            logging.info('X_UpgradeAll found')
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except Exception as e:
            logging.debug('X_UpgradeAll NOT found {}'.format(e))
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/X_UnitInfo.png', region=(1200, 40, 100, 100))
            logging.info('X_UnitInfo found')
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except Exception as e:
            logging.debug('X_UnitInfo NOT found {}'.format(e))
    if check_number == 2 or check_number is None:
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/Join.png', region=(825, 660, 80, 50))
            logging.info('Join found')
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except Exception as e:
            logging.debug('Join NOT found {}'.format(e))
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/Distortion2Confirm.png', region=(900, 780, 150, 80))
            logging.info('Distortion2Confirm found')
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except Exception as e:
            logging.debug('Distortion2Confirm NOT found {}'.format(e))
    if check_number == 3 or check_number is None:
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/XAirships.png', region=(650, 40, 70, 70))
            logging.info('XAirships found')
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except Exception as e:
            logging.debug('XAirships NOT found {}'.format(e))
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/XBuyUnitGems.png', region=(1185, 535, 70, 70))
            logging.info('XBuyUnitGems found')
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except Exception as e:
            logging.debug('XBuyUnitGems NOT found {}'.format(e))
    if check_number == 4 or check_number is None:
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/CancelRefresh.png', region=(1030, 700, 100, 50))
            logging.info('CancelRefresh found')
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except Exception as e:
            logging.debug('CancelRefresh NOT found {}'.format(e))
        try:
            if pyautogui.locateCenterOnScreen('./pictures/ServerConnectionLost.png', region=(900, 530, 120, 50)):
                logging.info('ServerConnectionLost found')
                reopen_game()
            else:
                logging.debug('ServerConnectionLost NOT found')
        except Exception as e:
            logging.debug('ServerConnectionLost NOT found {}'.format(e))
    if check_number == 5 or check_number is None:
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/XBuyUnit.png', region=(1200, 100, 65, 65))
            logging.info('XBuyUnit found')
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except Exception as e:
            logging.debug('XBuyUnit NOT found {}'.format(e))
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/Wait.png', region=(850, 530, 70, 40))
            logging.info('Wait found')
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except Exception as e:
            logging.debug('Wait {}'.format(e))
    if check_number == 6 or check_number is None:
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/AccessRewardConfirm.png', region=(900, 830, 120, 50))
            logging.info('AccessRewardConfirm found')
            pyautogui.click(x, y)
            time.sleep(wR.delay * 2 * 2)
        except Exception as e:
            logging.debug('AccessRewardConfirm NOT found {}'.format(e))
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/BuyAllConfirm2.png',
                                                  region=(890, 620, 150, 100))
            logging.info('BuyAllConfirm2 found')
            pyautogui.click(x, y)
            time.sleep(wR.delay*2)
        except Exception as e:
            logging.info('BuyAllConfirm2 NOT found {}'.format(e))
    if check_number == 7 or check_number is None:
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/AdditionalLevel.png',
                                                  region=(910, 850, 100, 40))
            logging.info('AdditionalLevel found')
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except Exception as e:
            logging.info('AdditionalLevel NOT found {}'.format(e))
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/SureRefreshCancel.png',
                                                  region=(1030, 680, 100, 40))
            logging.info('SureRefreshCancel found')
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except Exception as e:
            logging.info('SureRefreshCancel NOT found {}'.format(e))
    if check_number == 8 or check_number is None:
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/startConfirm.png', region=(910, 880, 100, 40))
            logging.info('startConfirm found')
            pyautogui.click(x, y)
            time.sleep(wR.delay * 2 * 2)
        except Exception as e:
            logging.error('startConfirm NOT found {}'.format(e))
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/BuyAllConfirm3.png',
                                                  region=(910, 660, 100, 40))
            logging.info('BuyAllConfirm3 found')
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except Exception as e:
            logging.info('BuyAllConfirm3 NOT found {}'.format(e))
    if check_number == 9 or check_number is None:
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/XNews.png', region=(1150, 840, 50, 50))
            logging.info('XNews found')
            pyautogui.click(x, y)
            time.sleep(wR.delay * 2 * 2)
        except Exception as e:
            logging.error('XNews NOT found {}'.format(e))
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/CancelBuyUnit.png', region=(990, 610, 120, 60))
            logging.info('CancelBuyUnit found')
            pyautogui.click(x, y)
            time.sleep(wR.delay * 2 * 2)
        except Exception as e:
            logging.error('CancelBuyUnit NOT found {}'.format(e))
    if check_number == 10 or check_number is None:
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/Distortion3Confirm.png', region=(900, 835, 120, 70))
            logging.info('Distortion3Confirm found')
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except Exception as e:
            logging.debug('Distortion3Confirm NOT found {}'.format(e))
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/quest_confirm.png', region=(875, 800, 150, 100))
            logging.info('quest_confirm found')
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except Exception as e:
            logging.debug('quest_confirm NOT found {}'.format(e))
    if check_number == 11 or check_number is None:
        while True:
            try:
                x, y = pyautogui.locateCenterOnScreen('./pictures/UnitsRecruitedConfirm.png',
                                                      region=(1060, 200, 200, 400))
                logging.info('UnitsRecruitedConfirm found')
                pyautogui.click(x, y)
                pyautogui.click(1120, 940)
                time.sleep(wR.delay)
                break
            except Exception as e:
                logging.debug('UnitsRecruitedConfirm NOT found {}'.format(e))
            try:
                x, y = pyautogui.locateCenterOnScreen('./pictures/UnitsRecruitedConfirm2.png',
                                                      region=(1060, 200, 200, 400))
                logging.info('UnitsRecruitedConfirm2 found')
                pyautogui.click(x, y)
                pyautogui.click(1120, 940)
                time.sleep(wR.delay)
                break
            except Exception as e:
                logging.debug('UnitsRecruitedConfirm2 NOT found {}'.format(e))
            try:
                x, y = pyautogui.locateCenterOnScreen('./pictures/UnitsRecruitedConfirm3.png',
                                                      region=(1060, 200, 200, 400))
                logging.info('UnitsRecruitedConfirm3 found')
                pyautogui.click(x, y)
                pyautogui.click(1120, 940)
                time.sleep(wR.delay)
                break
            except Exception as e:
                logging.debug('UnitsRecruitedConfirm3 NOT found {}'.format(e))
            try:
                x, y = pyautogui.locateCenterOnScreen('./pictures/UnitsRecruitedConfirm4.png',
                                                      region=(1060, 200, 200, 400))
                logging.info('UnitsRecruitedConfirm4 found')
                pyautogui.click(x, y)
                pyautogui.click(1120, 940)
                time.sleep(wR.delay)
                break
            except Exception as e:
                logging.debug('UnitsRecruitedConfirm4 NOT found {}'.format(e))
            break


def check_after_revive():
    revival_done = False
    while not revival_done:
        try:  # must
            x, y = pyautogui.locateCenterOnScreen('./pictures/ConfirmRevive.png', region=(910, 950, 100, 50))
            time.sleep(wR.delay * 2 * 5)
            logging.info('ConfirmRevive found')
            pyautogui.click(x, y)
            time.sleep(wR.delay * 2 * 20)
            revival_done = True
            try:  # maybe
                x, y = pyautogui.locateCenterOnScreen('./pictures/Join.png', region=(825, 660, 80, 50))
                logging.info('Join found')
                pyautogui.click(x, y)
                time.sleep(wR.delay * 10 * 2)
                while True:
                    try:  # maybe
                        x, y = pyautogui.locateCenterOnScreen('./pictures/JoinConfirm.png', region=(900, 650, 120, 50))
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
    return revival_done


def solve_code():
    return 0  # Until fixed..
    logging.info('solve_code')
    while not wR.is_solve_code:
        wR.is_solve_code = True
        time.sleep(wR.delay)
        image = './printscreens/code.png'
        im = pyautogui.screenshot(image, region=(825, 265, 265, 175))
        im.save(image)
        try:
            c = CodeDecipher(image)
        except Exception as e:
            print('solve_code - FAILED')
            logging.debug('solve_code - FAILED {}'.format(e))
            wR.is_solve_code = False
            return 0
        if not c.code:
            print('solve_code - FAILED. code is empty list')
            logging.debug('solve_code - FAILED. code is empty list')
            wR.is_solve_code = False
            return 0
        for each in c.code:
            x, y = image_search('./pictures/' + str(each) + '.png', region=(740, 583, 450, 340), precision=0.94)
            pyautogui.click(x, y)
            time.sleep(wR.delay)

        x, y = image_search('./pictures/CodeConfirm.png', region=(785, 990, 100, 40))
        pyautogui.click(x, y)
        time.sleep(wR.delay * 2 * 2)
        try:
            x, y = image_search('./pictures/CodeWrong.png', region=(915, 530, 90, 40))
            pyautogui.click(x, y)
            time.sleep(wR.delay)
            print('solve_code - FAILED')
            logging.debug('solve_code - FAILED')
            wR.is_solve_code = False
            return 0
        except Exception as e:
            time.sleep(wR.delay * 2 * 10)
            print('solve_code - SUCCESS')
            logging.info('solve_code - SUCCESS')
            wR.is_solve_code = False
            return 1


def reopen_game():
    logging.info('reopen_game')
    print('reopen_game')
    wR.is_reopen_game = True
    w.stopTimer()
    time.sleep(5)
    close_game()
    open_game()

    while True:
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/EndlessFrontier.png')
            logging.info('EndlessFrontier found')
            pyautogui.click(x, y)
            time.sleep(wR.delay)
            break
        except Exception as e:
            logging.error('EndlessFrontier NOT found {}'.format(e))
            time.sleep(wR.delay * 2)
    time.sleep(wR.delay * 2 * 5)
    while True:
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/fullScreen.png')
            logging.info('fullScreen found')
            pyautogui.click(x, y)
            time.sleep(wR.delay * 2 * 5)
            break
        except Exception as e:
            logging.error('fullScreen NOT found {}'.format(e))
            time.sleep(wR.delay * 2 )

    tmp_time = time.time()

    while time.time() - tmp_time < 180:
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/AccessRewardConfirm.png', region=(900, 830, 120, 50))
            logging.info('AccessRewardConfirm found')
            pyautogui.click(x, y)
            time.sleep(wR.delay * 2 * 2)
        except Exception as e:
            logging.debug('AccessRewardConfirm NOT found {}'.format(e))
            time.sleep(wR.delay)

        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/Distortion2Confirm.png', region=(900, 780, 150, 80))
            logging.info('Distortion2Confirm found')
            pyautogui.click(x, y)
            time.sleep(wR.delay * 2 * 2)
        except Exception as e:
            logging.debug('Distortion2Confirm NOT found {}'.format(e))
            time.sleep(wR.delay)

        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/startConfirm.png', region=(900, 870, 120, 60))
            logging.info('startConfirm found')
            pyautogui.click(x, y)
            time.sleep(wR.delay * 2 * 2)
        except Exception as e:
            logging.error('startConfirm NOT found {}'.format(e))
            time.sleep(wR.delay)

        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/XNews.png', region=(1150, 840, 50, 50))
            logging.info('XNews found')
            pyautogui.click(x, y)
            time.sleep(wR.delay * 2 * 2)
        except Exception as e:
            logging.error('XNews NOT found {}'.format(e))
            time.sleep(wR.delay)

    init()
    w.startTimer()
    wR.is_reopen_game = False
    logging.info('reopen_game - done')


def level_check():
    logging.info('level_check')
    if not wR.is_revive and not wR.is_solve_code and not wR.max_level_reached:
        try:
            if not wR.screen_saver_on:
                text = detect_level()
            else:
                text = detect_level(region=(959, 202, 48, 18))
            logging.debug('detected level = {}'.format(text))
            if wR.max_revive >= text > wR.min_lvl_detect:
                wR.filter.insert(0, text)
                wR.filter.pop()
            elif text == 0:
                wR.filter.insert(0, wR.filter[0])
                wR.filter.pop()
            logging.debug('wR.filter = {}'.format(wR.filter))
        except ValueError as e:
            wR.filter.insert(0, wR.filter[0])
            wR.filter.pop()
            logging.debug('wR.filter = {}'.format(wR.filter))
        finally:
            filtered_level = statistics.median(wR.filter)
            if filtered_level > wR.level_filter[0]:
                wR.level_filter.insert(0, filtered_level)
            else:
                wR.level_filter.insert(0, wR.level_filter[0])
            wR.level_filter.pop()
            logging.debug('filtered_level = {} wR.level_filter = {}'.format(filtered_level, wR.level_filter))
            
            if time.time() - wR.level_check_time >= 15:
                wR.level_check_time = time.time()
                logging.debug('statistics.median(wR.level_filter[:5]) = {}, statistics.median(wR.level_filter[-6:-1]) '
                              '= {}'.format(statistics.median(wR.level_filter[:5]), statistics.median(wR.level_filter[-6:-1])))
                logging.debug('Yes. statistics.median(wR.level_filter[:5]) - statistics.median(wR.level_filter[-6:-1]) < 10 ?')
                if statistics.median(wR.level_filter[:5]) - statistics.median(wR.level_filter[-6:-1]) < 10:
                    logging.debug('Yes. statistics.median(wR.level_filter) > 20800 ?')
                    if wR.level_filter[0] > wR.min_revive:
                        wR.max_level_reached = True
                        logging.debug('Yes. wR.max_level_reached = {}'.format(wR.max_level_reached))
                    else:
                        logging.debug('No.')
                else:
                    logging.debug('No.')
            else:
                logging.debug('No.')
                
            if (time.time() - wR.start_time > wR.MAX_MIN_TO_REV*60):
                wR.max_level_reached = True

            logging.debug('wR.max_level_reached ?')
            if wR.max_level_reached:
                logging.debug('Yes.')
                revive()
            else:
                logging.debug('No')
            logging.info('level_check - done')


def use_skills():
    logging.info('use_skills')
    level_check()
    if wR.exiting:
        return
    elif not wR.is_max_quests and not wR.is_upgrade_units and not wR.is_buy_units \
            and not wR.is_revive and not wR.is_reopen_game and not wR.is_use_skills \
            and not wR.is_solve_code:
        wR.is_use_skills = True

        if not wR.screen_saver_on:
            logging.info('clicking skills')
            pyautogui.click(875, 85)
            time.sleep(wR.delay_small)
            pyautogui.click(935, 85)
            time.sleep(wR.delay_small)
            pyautogui.click(995, 85)
            time.sleep(wR.delay_small)

    wR.is_use_skills = False
    logging.info('use_skills - done')
    wR.skills_timer = Timer(3, use_skills)
    wR.skills_timer.start()


def open_chests():
    logging.info('open_chests')
    if wR.exiting:
        return
    elif not wR.is_max_quests and not wR.is_upgrade_units and not wR.is_buy_units \
            and not wR.is_revive and not wR.is_reopen_game and not wR.is_open_chests \
            and not wR.is_solve_code:
        wR.is_open_chests = True

        if not wR.screen_saver_on:
            logging.info('clicking chests')
            pyautogui.click(1000, 360)
            time.sleep(wR.delay_small)
            pyautogui.click(920, 360)
            time.sleep(wR.delay_small)
            pyautogui.click(850, 360)
            time.sleep(wR.delay_small / 2)

        if wR.open_chests_counter % 5 == 0:
            check_popups(wR.check_number)
            wR.check_number += 1
            logging.debug('wR.open_chests_counter = {} wR.check_number = {}'.format(wR.open_chests_counter, wR.check_number))
            if wR.open_chests_counter >= 2000:
                wR.open_chests_counter = 0
            if wR.check_number >= 12:
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
    elif not wR.is_upgrade_units and not wR.is_buy_units and not wR.is_revive \
            and not wR.is_reopen_game and not wR.is_max_quests and not wR.is_solve_code:
        wR.is_max_quests = True
        drag_by = 102
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/quests.png', region=(660, 930, 100, 100))
            logging.info('quests found')
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except Exception as e:
            logging.debug('quests NOT found {}'.format(e))
        finally:
            first_time = 1
            if pyautogui.locateCenterOnScreen('./pictures/questsOn.png', region=(660, 930, 100, 100)):
                last_quest = 0
                last_drag = False
                num_of_drags = 0
                while True:
                    blacks = []
                    for x in range(600, 942, 4):  # search for click-able quests
                        if pyautogui.pixel(1235, x) == pyautogui.pixel(1235, x+1) == (8, 8, 8):
                            blacks.append(x)
                    pyautogui.moveTo(930, 770)
                    if not blacks:  # we dragged too much.. by accident ofcourse
                        if num_of_drags < 10:
                            num_of_drags += 1
                            check_popups()
                            pyautogui.dragRel(0, drag_by, 1, tween=pyautogui.easeOutQuad, button='left')
                        else:
                            for each in range(0, 10):
                                time.sleep(wR.delay)
                                pyautogui.moveTo(930, 770)
                                pyautogui.dragRel(0, -drag_by, 1, tween=pyautogui.easeOutQuad, button='left')
                            num_of_drags = 0
                    elif max(blacks) > 800 and not last_drag:  # if there is a potentially better quest to open
                        check_popups()
                        try:
                            x, y = pyautogui.locateCenterOnScreen('./pictures/last_drag_quest.png', region=(660, 737, 100, 100))
                            pyautogui.click(x, y)
                            last_drag = True
                        except Exception as e:
                            logging.debug('last_drag_quest.png NOT found {}'.format(e))
                            pyautogui.dragRel(0, -drag_by, 1, tween=pyautogui.easeOutQuad, button='left')
                    else:
                        last_quest = max(blacks)  # best quest to open
                        break
                    first_time = 0

                if last_quest != 0:
                    logging.debug('wR.quests_add_rel = {}'.format(wR.quests_add_rel))
                    for x in range(0, 5): # Click right
                        pyautogui.click(1180, last_quest)
                        time.sleep(wR.delay_small)
                    pyautogui.click(700, last_quest)
                    for x in range(0, 3): # Click left
                        pyautogui.click(900, last_quest)
                        time.sleep(wR.delay_small)
                    pyautogui.click(700, last_quest)

                    try:
                        x, y = pyautogui.locateCenterOnScreen('./pictures/quest_confirm.png', region=(875, 800, 150, 100))
                        logging.info('quest_confirm found')
                        if pyautogui.locateCenterOnScreen('./pictures/last_quest.png', region=(675, 545, 300, 120)):
                            logging.info('last_quest found')
                            pyautogui.click(x, y)
                            time.sleep(wR.delay)
                            wR.is_max_quests = False
                            logging.info('max_quests - done')
                            return
                        else:
                            pyautogui.click(x, y)
                            time.sleep(wR.delay)
                        wR.max_quests_counter = 0
                    except Exception as e:
                        logging.debug('quest_confirm NOT found {}'.format(e))
                        wR.max_quests_counter += 1
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
    elif not wR.is_upgrade_units and not wR.is_max_quests and not wR.is_revive \
            and not wR.is_reopen_game and not wR.is_buy_units and not wR.is_solve_code:
        wR.is_buy_units = True
        time.sleep(wR.delay * 4)
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/Unit.png', region=(750, 935, 200, 100))
            logging.info('Unit found')
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except Exception as e:
            logging.debug('Unit NOT found {}'.format(e))
            try:
                x, y = pyautogui.locateCenterOnScreen('./pictures/quests.png', region=(645, 930, 120, 100))
                logging.info('quests found')
                pyautogui.click(x, y)
                time.sleep(wR.delay)
                x, y = pyautogui.locateCenterOnScreen('./pictures/Unit.png', region=(750, 935, 200, 100))
                logging.info('Unit found')
                pyautogui.click(x, y)
                time.sleep(wR.delay)
            except Exception as e:
                logging.debug('quests / Unit NOT found {}'.format(e))
        finally:
            try:
                x, y = pyautogui.locateCenterOnScreen('./pictures/BuyUnit.png', region=(1170, 520, 100, 65))
                logging.info('BuyUnit found')
                pyautogui.click(x, y)
                time.sleep(wR.delay)
                try:
                    x, y = pyautogui.locateCenterOnScreen('./pictures/Refresh.png', region=(1120, 520, 100, 100))
                    logging.info('Refresh found')
                    time.sleep(wR.delay * 2 * 2)
                    pyautogui.click(x, y)
                    time.sleep(wR.delay * 2 * 2)
                    done = False
                    try:
                        x, y = pyautogui.locateCenterOnScreen('./pictures/RefreshUnitListCancel.png', region=(1020, 700, 100, 50))
                        logging.debug('RefreshUnitListCancel found')
                        pyautogui.click(x, y)
                    except:
                        while not done:
                            try:
                                x, y = pyautogui.locateCenterOnScreen('./pictures/BuyAll.png', region=(950, 520, 90, 60))
                                logging.info('BuyAll found')
                                pyautogui.click(x, y)
                                time.sleep(wR.delay)
                                while not done:
                                    try:
                                        x, y = pyautogui.locateCenterOnScreen('./pictures/BuyAllConfirm.png',
                                                                              region=(800, 590, 150, 100))
                                        logging.info('BuyAllConfirm found')
                                        pyautogui.click(x, y)
                                        time.sleep(wR.delay)
                                        while not done:
                                            try:
                                                x, y = pyautogui.locateCenterOnScreen('./pictures/BuyAllConfirm2.png',
                                                                                      region=(890, 620, 150, 100))
                                                logging.info('BuyAllConfirm2 found')
                                                pyautogui.click(x, y)
                                                time.sleep(wR.delay*2)
                                                done = True
                                            except Exception as e:
                                                logging.debug('BuyAllConfirm2 NOT found {}'.format(e))
                                                try:
                                                    x, y = pyautogui.locateCenterOnScreen('./pictures/BuyAllConfirm3.png',
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
                                    x, y = pyautogui.locateCenterOnScreen('./pictures/UnitsRefreshingConfirm.png',
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
    elif not wR.is_buy_units and not wR.is_max_quests and not wR.is_revive \
            and not wR.is_reopen_game and not wR.is_upgrade_units and not wR.is_solve_code:
        wR.is_upgrade_units = True
        try:
            x, y = pyautogui.locateCenterOnScreen('./pictures/Unit.png', region=(750, 935, 200, 100))
            logging.info('Unit found')
            pyautogui.click(x, y)
            time.sleep(wR.delay)
        except Exception as e:
            logging.debug('Unit NOT found {}'.format(e))
            try:
                x, y = pyautogui.locateCenterOnScreen('./pictures/quests.png', region=(645, 930, 120, 100))
                logging.info('quests found')
                pyautogui.click(x, y)
                time.sleep(wR.delay)
                x, y = pyautogui.locateCenterOnScreen('./pictures/Unit.png', region=(750, 935, 200, 100))
                logging.info('Unit found')
                pyautogui.click(x, y)
                time.sleep(wR.delay)
            except Exception as e:
                logging.debug('Unit/quests NOT found {}'.format(e))
        finally:
            if pyautogui.locateCenterOnScreen('./pictures/UnitOn.png', region=(750, 935, 200, 100)):
                logging.debug('wR.upgraded_units_once = {}'.format(wR.upgraded_units_once))
                if time.time() - wR.start_time > 10*60:
                    if not wR.upgraded_units_once:
                        try:
                            x, y = pyautogui.locateCenterOnScreen('./pictures/UpgradeAll.png', region=(970, 520, 90, 70))
                            logging.info('UpgradeAll found')
                            pyautogui.click(x, y)
                            time.sleep(wR.delay)
                            for x in range(4):
                                pyautogui.click(745 + 143 * x, 410, clicks=5, interval=wR.delay_small)
                            time.sleep(wR.delay)
                            x, y = pyautogui.locateCenterOnScreen('./pictures/X_UpgradeAll.png', region=(1175, 175, 100, 100))
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
                            x, y = pyautogui.locateCenterOnScreen('./pictures/X_UnitInfo.png', region=(1200, 30, 100, 200))
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
                            x, y = pyautogui.locateCenterOnScreen('./pictures/X_UnitInfo.png', region=(1200, 30, 100, 200))
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
