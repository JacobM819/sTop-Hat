from selenium import webdriver
from selenium.common import NoSuchWindowException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from threading import Thread
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
        self.thread = Thread(target=self.runBot)

    def login(self, driver):
        # If on TopHat enter school page
        if onPage(driver, By.ID, "select-input-1"):
            element = driver.find_element(By.ID, "select-input-1")
            element.clear()
            element.send_keys(self.school)
            time.sleep(1)
            element.send_keys(Keys.ENTER)
        # If asked to SSO with school account system
        if onPage(driver, By.CLASS_NAME, "fFskqF"):
            element = driver.find_element(By.CLASS_NAME, "fFskqF")
            element.click()
            time.sleep(2)
        # If on Outlook login page
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
        driver = webdriver.Chrome()
        driver.get("https://app.tophat.com/")
        while True:
            try:
                time.sleep(3)
                # If on any stage of the login page
                if onPage(driver, By.ID, "select-input-1") or onPage(driver, By.NAME, "loginfmt") or onPage(driver, By.NAME, "passwd"):
                    self.login(driver)
                    print(f"logging in: {self.email}")
                    pass
                # If there is an unanswered question, answer it
                elif onPage(driver, By.CLASS_NAME, "list-row--unanswered"):
                    answerQuestion(driver)
                    pass
                # If at home screen, open requested class
                elif driver.current_url == "https://app.tophat.com/e":
                    print(f"At homescreen: open class {self.class_code}")
                    driver.get(f"https://app.tophat.com/e/{self.class_code}")
                    pass
                else:
                    print("no question found")
                    time.sleep(7)
            # If the browser was closed, quit the program
            except NoSuchWindowException:
                print("closing window...")
                driver.quit()
                break

    def startMultiBot(self):
        self.thread.start()


jacob = Student("Pennsylvania State University (Penn State)", "jrm7250@psu.edu", "Ringgold819", "849492")
# bryan = Student("Pennsylvania State University (Penn State)", "bdn5122@psu.edu", "Ponies#5888", "849492")
# janel = Student("Pennsylvania State University (Penn State)", "bdn5122@psu.edu", "Ponies#5888", "849492")

jacob.startMultiBot()
# bryan.startMultiBot()
# janel.startMultiBot()
