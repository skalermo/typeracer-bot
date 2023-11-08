from PySide2.QtCore import QTimer
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from pynput.keyboard import Controller
import pyautogui
from selenium.webdriver.common.by import By


class Bot:
    def __init__(self):
        self.current_timer = None
        self._init_timer()

        self._text_iter = None
        self.keyboard = Controller()

        # typing speed in wpm
        self.typing_speed = 100
        self.expected_time_s = 0
        self.typing_delay_s = 1

        self.text_to_type = ''

        self.driver = webdriver.Firefox()
        self.driver.set_window_size(1200, 800)
        self.driver.set_window_position(0, 0)
        self.driver.switch_to.window(self.driver.current_window_handle)

        self.actions = ActionChains(self.driver)

        self.driver.get("https://play.typeracer.com/")

    def __del__(self):
        if self.driver:
            self.driver.close()

    def get_text(self):
        element = self.driver.find_element(By.CLASS_NAME, 'mainViewport')
        try:
            element = element.find_element(By.CLASS_NAME, 'gameView')
        except NoSuchElementException:
            return ''

        element = element.find_element(By.CLASS_NAME, 'inputPanel')
        self.text_to_type = element.text.split('\n')[0]
        self._calc_typing_delay()

    def start_race(self):
        self._focus_on_input_box()
        self._start_timer()

    def _enter_next_character(self):
        try:
            char = next(self._text_iter)
            self.keyboard.type(char)
        except StopIteration:
            self._stop_timer()

    def update_speed(self, new_speed):
        self.typing_speed = new_speed
        if self.text_to_type:
            self._calc_typing_delay()

    def _calc_typing_delay(self):
        word_count = len(self.text_to_type.split())
        self.expected_time_s = word_count / self.typing_speed * 60
        self.typing_delay_s = self.expected_time_s / len(self.text_to_type)

    def _focus_on_input_box(self):
        last_pos = pyautogui.position()
        pyautogui.click(100, 100)
        element = self.driver.find_element(By.CLASS_NAME, 'txtInput')
        element.click()
        pyautogui.moveTo(*last_pos)

    def _init_timer(self):
        self.current_timer = QTimer()
        self.current_timer.timeout.connect(self._enter_next_character)

    def _start_timer(self):
        self._text_iter = iter(self.text_to_type)
        if self.current_timer.isActive():
            self._stop_timer()
        self.current_timer.start(self.typing_delay_s * 1000)

    def _stop_timer(self):
        self.current_timer.stop()

