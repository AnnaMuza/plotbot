# -*- coding: utf-8 -*-

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException

THEME = '1'
GRID = 0

#FUNCTIONS
def change_theme_out(call):
    global THEME
    THEME = call.data

def get_theme():
    global THEME
    return THEME

def change_grid_out(call):
    global GRID
    if call.data == 'on':
        GRID = 1
        return 'Сетка включена!'
    else:
        GRID = 0
        return 'Сетка выключена!'

def get_grid():
    global GRID
    return GRID

def add_bd(chat):
    if chat.username:
        name = '@{} '.format(chat.username)
    else:
        if chat.first_name:
            name = '{} {} '.format(chat.first_name, chat.last_name)
        else:
            name = '"{}" '.format(chat.title)
    output = ''.join((name, str(chat.id), '\n'))
    with open('users.txt', 'r') as f:
        users = f.readlines()
    if not output in users:
        with open('users.txt', 'a', encoding="utf-8") as f:
            f.write(output)

def selenium(message):
    def plot_type():
        a = driver.find_element_by_xpath("/html/body/div[1]/div/div/main/div[2]/div/div[2]/div[1]/section/section[2]/header/h2")
        return 6 if not '3D' in a.text else 18

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    # driver = webdriver.Firefox()

    driver.implicitly_wait(3)
    driver.get("https://www.wolframalpha.com/input/?i="+requests.utils.quote(message.text.lower()))
    driver.set_window_size(1920, 1080)
    try:
        WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/main/div[2]/div/div[2]/div[1]/section/section[2]/div/div/img')))
    except TimeoutException:
        return False, 'К сожалению, бот не может построить данный график. Проверьте правильность ввода'

    RENDER_TIME = plot_type()

    accept_cookies = driver.find_element_by_xpath('/html/body/div[1]/div/section/button')
    accept_cookies.click()

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    plot = driver.find_element_by_xpath("/html/body/div[1]/div/div/main/div[2]/div/div[2]/div[1]/section/section[2]/div")
    hover = ActionChains(driver).move_to_element(plot)
    hover.perform()

    try:
        element = driver.find_element_by_xpath("/html/body/div[1]/div/div/main/div[2]/div/div[2]/div[1]/section/section[2]/ul/li[3]/button")
    except NoSuchElementException:
        element = driver.find_element_by_xpath("/html/body/div[1]/div/div/main/div[2]/div/div[2]/div[1]/section/section[2]/ul/li[2]/button")
    element.click()

    select_theme = driver.find_element_by_xpath("/html/body/div[1]/div/div/main/div[2]/div/div[2]/div[1]/section/section[3]/section/section[1]/div[1]/div/button[{}]".format(THEME))
    select_theme.click()

    # include_input = driver.find_element_by_xpath("/html/body/div[1]/div/div/main/div[2]/div/div[2]/div[1]/section/section[3]/section/section[1]/div[2]/div/div[1]/button")
    # include_input.click()

    size = driver.find_element_by_xpath("/html/body/div[1]/div/div/main/div[2]/div/div[2]/div[1]/section/section[3]/section/section[1]/div[5]/div/button")
    size.click()

    size_large = driver.find_element_by_xpath("/html/body/div[1]/div/div/main/div[2]/div/div[2]/div[1]/section/section[3]/section/section[1]/div[5]/div/ul/li[3]/button")
    size_large.click()

    add_bd(message.chat)
    time.sleep(RENDER_TIME)

    img = driver.find_element_by_xpath("/html/body/div[1]/div/div/main/div[2]/div/div[2]/div[1]/section/section[3]/section/section[2]/img")
    src = img.get_attribute('src')
    driver.quit()

    image = requests.get(src)
    return True, image