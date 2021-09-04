from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import urllib
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image_dataset_from_directory
import uuid
import os, requests
from selenium.webdriver.remote.webelement import WebElement
from typing import List
import cv2
import pytesseract 
import time
import telebot
#logging.basicConfig(level=logging.DEBUG)

bot = telebot.TeleBot(token="1993230425:AAEqbDCNCDGDcAJ00w1nBmk9loenYbMRcbc")

batch_size = 32
image_size = (254, 254)
model = load_model("crypto_checking_network_vID.h5")

options = Options()
options.headless = True
driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver', options=options)
driver.implicitly_wait(5)
driver.get('https://twitter.com/nd6q4X6qTYcbZCV')
driver.implicitly_wait(5)
card = driver.find_element_by_xpath('//div[@data-testid="tweet"]')
driver.implicitly_wait(5)
time_post = card.find_element_by_xpath('.//time').get_attribute('datetime')
last_time = time_post
trigger = False


def get_image(container):
    try:
        driver.implicitly_wait(10)
        images:List[WebElement] = container.find_elements_by_xpath('.//img')
        print(len(images))
        time.sleep(0.05)
        del images[0]
        if len(images) < 2:
            imname = uuid.uuid4()
            src = images[0].get_attribute('src')
            urllib.request.urlretrieve(src, f'/projects/im/ims/{imname}.jpg')
            print('IMAGE SAVE SUCCESsS')
        else:
            for element in images:
                imname = uuid.uuid4()
                src = element.get_attribute('src')
                urllib.request.urlretrieve(src, f'/projects/im/ims/{imname}.jpg')
                print('IMAGE SAVE SUCCESsS')
    except Exception as e:
        print('ERROR SAVE IMAGE')
        print(e)

def get_text(card):
    global trigger
    try:
        text = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
        if 'doge' in text or 'shib' in text:
            trigger = True
            print('DOUG')
            bot.send_message('488664136', 'DOGE')
            r = requests.get('http://45.137.64.175:2000/ZldaOUMyTlBiU1hFdWpYRkZUbUFFNjdv/SHIB')
        print(text)
    except Exception as e:
        print('TEXT_ERROR')
        print(e)

def check_image_text():
    global trigger
    try:
        images = os.listdir('/projects/im/ims/')
        for img in images:
            if not trigger:
                img = cv2.imread(f'/projects/im/ims/{img}')
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                res = pytesseract.image_to_string(img)
                res = res.lower()
                print(res)
                if 'doge' in res or 'shib' in res:
                    trigger = True
                    print('DOUG')
                    bot.send_message('488664136', 'DOGE')
                    r = requests.get('http://45.137.64.175:2000/ZldaOUMyTlBiU1hFdWpYRkZUbUFFNjdv/SHIB')
    except Exception as e:
        print('text_img_ERROR')
        print(e)

def check_image():
    global trigger
    try:
        images = os.listdir('/projects/im/ims/')
        for img in images:
            img = cv2.imread(f'/projects/im/ims/{img}')
            img = cv2.resize(img, (254,254), interpolation=cv2.INTER_AREA)
            cv2.imwrite(f'/projects/im/ims/{img}.jpg', img)

        test_dataset = image_dataset_from_directory('/projects/im/',
                                                batch_size=batch_size,
                                                image_size=image_size)
        res = model.predict(test_dataset)
        for pic in res:
            if not trigger:
                if pic[1] > 0.5 or pic[4] > 0.5 or pic[8] > 0.5:
                    print('DOUG')
                    bot.send_message('488664136', 'DOGE')
                    r = requests.get('http://45.137.64.175:2000/ZldaOUMyTlBiU1hFdWpYRkZUbUFFNjdv/SHIB')
                    trigger = True
    except Exception as e:
        print('CHECKING_ERROR')
        print(e)
#//div[2]/div[2]

def check_tweets(l_t):
    try:
        last_time = l_t
        global trigger
        global driver
        while True:
            driver.implicitly_wait(10)
            container:WebElement = driver.find_element_by_xpath('//div[@data-testid="tweet"]')
            time_post = container.find_element_by_xpath('.//time').get_attribute('datetime')

            if time_post != last_time:
                get_text(container)
                if not trigger:
                    get_image(container)
                    check_image_text()
                    check_image() 
                trigger = False
                for elem in os.listdir('/projects/im/ims/'):
                    os.remove(f'/projects/im/ims/{elem}')
            last_time = time_post
            driver.refresh()
            driver.implicitly_wait(5)
    except Exception as e:
        print(e)
        print('***************************************************************************************')
        print('Перезагрузка сервера')
        print('***************************************************************************************')
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver', options=options)
        driver.implicitly_wait(5)
        driver.get('https://twitter.com/IKudryavtzeff')
        driver.implicitly_wait(5)
        card = driver.find_element_by_xpath('//div[@data-testid="tweet"]')
        driver.implicitly_wait(5)
        time_post = card.find_element_by_xpath('.//time').get_attribute('datetime')
        last_time = time_post
        trigger = False
        check_tweets(last_time)

check_tweets(last_time)
bot.polling()