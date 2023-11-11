import numpy as np
import requests
from PySide2.QtCore import QTimer
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from pynput.keyboard import Controller
import pyautogui
from selenium.webdriver.common.by import By

from challenge_solver.ocr import read_from_challenge_image


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

    def _focus_on_input_box(self, box_class_name: str = 'txtInput'):
        last_pos = pyautogui.position()
        pyautogui.click(100, 100)
        element = self.driver.find_element(By.CLASS_NAME, box_class_name)
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

    def is_challenged(self):
        elements_detected = len(self.driver.find_elements(By.CLASS_NAME, 'challengePromptDialog')) + len(self.driver.find_elements(By.CLASS_NAME, 'typingChallengeDialog'))
        return elements_detected >= 1

    def is_challenge_not_accepted(self):
        return len(self.driver.find_elements(By.CLASS_NAME, 'challengePromptDialog')) >= 1

    def accept_challenge(self):
        button = self.driver.find_element(By.CLASS_NAME, 'challengePromptDialog').find_element(By.TAG_NAME, 'button')
        button.click()
        
    def solve_challenge(self):
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'typingChallengeDialog')))
        im = self._get_challenge_image()
        text = read_from_challenge_image(im)
        print(f'Detected text: "{text}"')
        self._type_in_challenge_text(text)

    def _get_challenge_image(self):
        src = self.driver.find_element(By.CLASS_NAME, 'typingChallengeDialog').find_element(By.CLASS_NAME, 'challengeImg').get_attribute('src')
        res = requests.get(src, stream=True).raw
        return np.asarray(bytearray(res.read()), dtype="uint8")

    def _type_in_challenge_text(self, text: str):
        self.text_to_type = text
        self._calc_typing_delay()
        self._focus_on_input_box('challengeTextArea')
        self._start_timer()
