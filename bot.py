from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from pynput.keyboard import Controller
import pyautogui


class Bot:
    def __init__(self):
        # self.timer = timer
        # self.timer.timeout.connect()
        self.keyboard = Controller()

        # typing speed in wpm
        self.typing_speed = 100
        self.expected_time_s = 0
        self.typing_delay = 1

        self.text_to_type = ''

        self.driver = webdriver.Firefox(firefox_profile=webdriver.FirefoxProfile())
        self.driver.set_window_size(1200, 800)
        self.driver.set_window_position(0, 0)
        self.driver.switch_to.window(self.driver.current_window_handle)

        self.actions = ActionChains(self.driver)

        self.driver.get("https://play.typeracer.com/")

    def __del__(self):
        if self.driver:
            self.driver.close()

    def get_text(self):
        element = self.driver.find_element_by_class_name('mainViewport')
        try:
            element = element.find_element_by_class_name('gameView')
        except NoSuchElementException:
            return ''

        element = element.find_element_by_class_name('inputPanel')
        ids = element.find_elements_by_xpath('//*[@id]')

        text = ''
        for ii in ids:
            if ii.tag_name == 'td':
                etx = ii.text.find('change display format')
                stx = ii.text.rfind('0 wpm') + 6
                text = ii.text[stx:etx]
                break
        self.text_to_type = text
        self._calc_typing_delay()

    def start_race(self):
        self._focus_on_input_box()
        for char in self.text_to_type:
            self._enter_character(char)

    def _enter_character(self, char):
        sleep(self.typing_delay)
        self.keyboard.type(char)

    def update_speed(self, new_speed):
        self.typing_speed = new_speed
        if self.text_to_type:
            self._calc_typing_delay()

    def _calc_typing_delay(self):
        word_count = len(self.text_to_type.split())
        self.expected_time_s = word_count / self.typing_speed * 60
        self.typing_delay = self.expected_time_s / len(self.text_to_type)

    def _focus_on_input_box(self):
        pyautogui.click(100, 100)
        element = self.driver.find_element_by_class_name('txtInput')
        element.click()
