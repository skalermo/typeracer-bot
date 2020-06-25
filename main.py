from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from time import sleep
from pynput.keyboard import Controller


def get_rid_of_popup_window(driver):
    try:
        close_privacy_content = driver.find_element_by_class_name('qc-cmp-ui-content')
        close_privacy_box = close_privacy_content.find_elements_by_id('qcCmpButtons')
        close_privacy_button = close_privacy_box[0].find_element_by_class_name('qc-cmp-button')
        close_privacy_button.click()
    except NoSuchElementException:
        pass


def enter_the_first_game(driver):
    print('Starting to enter ctrl+alt+I...')
    ActionChains(driver).key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys('I').key_up(Keys.CONTROL).perform()
    print('Entered keyboard combination')


def get_text(driver):
    element = driver.find_element_by_class_name('mainViewport')
    element = element.find_element_by_class_name('gameView')
    element = element.find_element_by_class_name('inputPanel')
    ids = element.find_elements_by_xpath('//*[@id]')

    text = ''
    for ii in ids:
        if ii.tag_name == 'td':
            etx = ii.text.find('change display format')
            stx = ii.text.rfind('0 wpm') + 6
            text = ii.text[stx:etx]
            break
    return text


def wait_until_race_starts(driver):
    timeDisplay = driver.find_element_by_class_name('timeDisplay')
    time = timeDisplay.find_element_by_class_name('time')

    time = int(time.text[-2:]) - 44
    if time < 0:
        time = 10
    print(f'Calculated time to start: {time}')
    for i in list(range(time))[::-1]:
        print(i)
        sleep(1)


def enter_character(keyboard, char, delay):
    keyboard.type(char)
    sleep(delay)


def main():
    keyboard = Controller()
    driver = webdriver.Firefox(firefox_profile=webdriver.FirefoxProfile())
    actions = ActionChains(driver)

    driver.get("https://play.typeracer.com/")
    sleep(1)
    get_rid_of_popup_window(driver)

    sleep(1)

    enter_the_first_game(driver)

    sleep(1)

    text = get_text(driver)
    word_count = len(text.split())
    print(text)

    wait_until_race_starts(driver)

    speed_wpm = 100
    expected_time_s = word_count/speed_wpm*60
    speed_spc = expected_time_s/len(text)
    print(f'Seconds per character = {speed_spc}')

    delay = speed_spc*0.8

    for char in text:
        enter_character(keyboard, char, speed_spc)

    # print()

    input('Press enter to quit...')
    driver.quit()


if __name__ == '__main__':
    main()




