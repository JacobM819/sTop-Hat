from selenium import webdriver
from selenium.common import NoSuchWindowException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


def onPage(driver, type, name):
    try:
        driver.find_element(type, name)
    except:
        return False
    return True


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


class Student:
    def __init__(self, school, email, password, class_code):
        self.school = school
        self.email = email
        self.password = password
        self.class_code = class_code

    def login(self, driver):
        if onPage(driver, By.ID, "select-input-1"):
            element = driver.find_element(By.ID, "select-input-1")
            element.clear()
            element.send_keys(self.school)
            time.sleep(2)
            element.send_keys(Keys.ENTER)
        if onPage(driver, By.CLASS_NAME, "fFskqF"):
            element = driver.find_element(By.CLASS_NAME, "fFskqF")
            element.click()
            time.sleep(3)
        elif onPage(driver, By.NAME, "loginfmt"):
            try:
                element = driver.find_element(By.NAME, "loginfmt")
                element.clear()
                element.send_keys(self.email)
                element.send_keys(Keys.ENTER)
                time.sleep(2)
                element = driver.find_element(By.NAME, "passwd")
                element.clear()
                element.send_keys(self.password)
                time.sleep(2)
                element.send_keys(Keys.ENTER)
                print("Duo Security")
                time.sleep(10)
            except NoSuchElementException:
                print("Login not found")


    def runBot(self):
        clock = 1000
        driver = webdriver.Chrome()
        driver.get("https://app.tophat.com/")
        while clock > 0:
            time.sleep(3)
            # If on login page
            if onPage(driver, By.ID, "select-input-1") or onPage(driver, By.NAME, "loginfmt") or onPage(driver, By.NAME, "passwd"):
                self.login(driver)
                print("logging in")
                pass
            # If there is an unanswered question, answer it
            elif onPage(driver, By.CLASS_NAME, "list-row--unanswered"):
                answerQuestion(driver)
                pass
            # If at home screen, open requested class
            elif driver.current_url == "https://app.tophat.com/e":
                print("At homescreen")
                driver.get(f"https://app.tophat.com/e/{self.class_code}")
                pass
            else:
                print("no question found")
            clock -= 1


jacob = Student("Pennsylvania State University (Penn State)", "jrm7250@psu.edu", "Ringgold819", "849492")
jacob.runBot()
