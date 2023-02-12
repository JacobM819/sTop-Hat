from selenium import webdriver
from selenium.common import NoSuchWindowException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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
    element.send_keys("American Heritage University")
    time.sleep(2)
    element.send_keys(Keys.ENTER)
    if onPage(driver, By.ID, "username"):
        element = driver.find_element(By.ID, "username")
        element.clear()
        element.send_keys("bryandn1210@gmail.com")
        element = driver.find_element(By.ID, "password")
        element.clear()
        element.send_keys("Ringgold819")
        time.sleep(2)
        element.send_keys(Keys.ENTER)


def answerQuestion(driver):
    # Find unanswered question
    question = driver.find_element(By.CLASS_NAME, "list-row--unanswered")
    question.click()
    time.sleep(5)
    # Find answer
    if onPage(driver, By.TAG_NAME, "label"):
        answer = driver.find_element(By.TAG_NAME, "label")
        print("answer found")
        answer.click()
        time.sleep(2)
        # Find submit button
        if onPage(driver, By.CLASS_NAME, "kerHW"):
            try:
                submit = driver.find_element(By.CLASS_NAME, "kerHW")
                submit.click()
            except:
                print("cannot submit")
            print("question answered")
    else:
        print("question not found")


def run():
    clock = 1000
    driver = webdriver.Chrome()
    driver.get("https://app.tophat.com/")
    while clock > 0:
        time.sleep(3)
        # If on login page
        if onPage(driver, By.ID, "select-input-1"):
            login(driver)
            print("logging in")
            pass
        # If on question page
        elif onPage(driver, By.CLASS_NAME, "list-row--unanswered"):
            answerQuestion(driver)
            pass
        else:
            print("no question found")
        clock -= 1
        # driver.refresh()


run()
