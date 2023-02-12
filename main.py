import selenium
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def onPage(driver, type, name):
    try:
        driver.find_element(type, name)
    except:
        return False
    return True


def login(driver):
    element = driver.find_element(By.ID, "select-input-1")
    element.clear()
    element.send_keys("American Heritage University", Keys.ENTER)
    if onPage(driver, By.ID, "username"):
        element = driver.find_element(By.ID, "username")
        element.clear()
        element.send_keys("bryandn1210@gmail.com")
        element = driver.find_element(By.ID, "password")
        element.clear()
        element.send_keys("Ringgold819", Keys.ENTER)


def answerQuestion(driver):
    question = driver.find_element(By.CLASS_NAME, "list-row--unanswered")
    question.click()


def run():
    clock = 1000
    driver = webdriver.Chrome()
    driver.get("https://app.tophat.com/")
    while clock > 0:
        if onPage(driver, By.ID, "select-input-1"):
            login(driver)
        elif onPage(driver, By.CLASS_NAME, "list-row--unanswered"):
            answerQuestion(driver)
        else:
            print("Nothing Found")
        clock -= 1
        time .sleep(10)
        driver.refresh()
    driver.close()


run()
