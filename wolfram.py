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
def change_theme_out(message):
    global THEME
    THEME = message.text

def change_grid_out(message):
    global GRID
    if message.text == 'Включить':
        GRID = 1
        return 'Сетка включена!'
    else:
        GRID = 0
        return 'Сетка выключена!'

def string_request(a):
    x = a.text[5:]
    x = x.replace('+', '%2B')
    x = x.replace('/', '%2F')
    x = x.replace('=', '%3D')
    x = x.replace(' ', '+')
    x += '+grid'*GRID
    return x

def selenium(a):
    def plot_type():
        a = driver.find_element_by_xpath("/html/body/div[1]/div/div/main/div[2]/div[2]/div[1]/section/section[2]/header/h2")
        return 15 if a.text == '3D plot:' else 5

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    # driver = webdriver.Firefox()
    driver.implicitly_wait(3)
    driver.get("https://www.wolframalpha.com/input/?i=plot+{}".format(string_request(a)))
    driver.set_window_size(1920, 1080)
    try:
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/main/div[2]/div[2]/div[1]/section/section[2]/div/div/img')))
    except TimeoutException:
        return False, 'К сожалению, бот не может построить данный график'

    RENDER_TIME = plot_type()

    accept_cookies = driver.find_element_by_xpath('/html/body/div[1]/div/section/button')
    accept_cookies.click()

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    plot = driver.find_element_by_xpath("/html/body/div[1]/div/div/main/div[2]/div[2]/div[1]/section/section[2]/div")
    hover = ActionChains(driver).move_to_element(plot)
    hover.perform()

    try:
        element = driver.find_element_by_xpath("/html/body/div[1]/div/div/main/div[2]/div[2]/div[1]/section/section[2]/ul/li[3]/button")
    except NoSuchElementException:
        element = driver.find_element_by_xpath("/html/body/div[1]/div/div/main/div[2]/div[2]/div[1]/section/section[2]/ul/li[2]/button")
    element.click()

    select_theme = driver.find_element_by_xpath("/html/body/div[1]/div/div/main/div[2]/div[2]/div[1]/section/section[3]/section/section[1]/div[1]/div/button[{}]".format(THEME))
    select_theme.click()

    # include_input = driver.find_element_by_xpath("/html/body/div[1]/div/div/main/div[2]/div[2]/div[1]/section/section[3]/section/section[1]/div[2]/div/div[1]/button")
    # include_input.click()

    size = driver.find_element_by_xpath("/html/body/div[1]/div/div/main/div[2]/div[2]/div[1]/section/section[3]/section/section[1]/div[5]/div/button")
    size.click()

    size_large = driver.find_element_by_xpath("/html/body/div[1]/div/div/main/div[2]/div[2]/div[1]/section/section[3]/section/section[1]/div[5]/div/ul/li[3]/button")
    size_large.click()

    time.sleep(RENDER_TIME)
    img = driver.find_element_by_xpath("/html/body/div[1]/div/div/main/div[2]/div[2]/div[1]/section/section[3]/section/section[2]/img")
    src = img.get_attribute('src')
    driver.quit()

    image = requests.get(src)
    return True, image