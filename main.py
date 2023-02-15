from selenium import webdriver
from selenium.common import NoSuchWindowException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from threading import Thread
import time
import random


def onPage(driver, type, name):
    try:
        driver.find_element(type, name)
    except:
        return False
    return True

def findRandomAnswer(driver):
    answer = driver.find_element(By.TAG_NAME, "input")
    answer_id = answer.get_attribute("id")[:-1]
    print(f"answer found: {answer_id}")
    answer_num = 0
    while True:
        try:
            answer = driver.find_element(By.ID, answer_id + str(answer_num))
        except NoSuchElementException:
            break
        answer_num += 1
    if answer_num == 0:
        return driver.find_element(By.ID, answer_id + "0")
    else:
        return driver.find_element(By.ID, answer_id + str(random.randint(0, answer_num-1)))


def answerQuestion(driver):
    # Find unanswered question
    try:
        question = driver.find_element(By.CLASS_NAME, "list-row--unanswered")
        question.click()
    except:
        return
    time.sleep(5)
    # Find answer
    if onPage(driver, By.TAG_NAME, "input"):
        answer = findRandomAnswer(driver)
        print("answer found")
        driver.execute_script("arguments[0].click();", answer)
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
            school_input = driver.find_element(By.ID, "select-input-1")
            school_input.clear()
            school_input.send_keys(self.school)
            time.sleep(1)
            school_input.send_keys(Keys.ENTER)
        # If asked to login through TopHat
        if onPage(driver, By.ID, "username"):
            print("username")
            username_input = driver.find_element(By.ID, "username")
            username_input.clear()
            username_input.send_keys(f"{self.email}")
            password_input = driver.find_element(By.ID, "password")
            password_input.clear()
            password_input.send_keys(f"{self.password}")
            if onPage(driver, By.CLASS_NAME, "joBsIl"):
                login_button = driver.find_element(By.CLASS_NAME, "joBsIl")
                login_button.click()
            time.sleep(2)
        # If on Outlook login page
        elif onPage(driver, By.CLASS_NAME, "fFskqF"):
            print("Outlook")
            login_button = driver.find_element(By.CLASS_NAME, "fFskqF")
            login_button.click()
            time.sleep(3)
        if onPage(driver, By.NAME, "loginfmt"):
            try:
                email_input = driver.find_element(By.NAME, "loginfmt")
                email_input.clear()
                email_input.send_keys(self.email)
                email_input.send_keys(Keys.ENTER)
                time.sleep(2)
                pswd_input = driver.find_element(By.NAME, "passwd")
                pswd_input.clear()
                pswd_input.send_keys(self.password)
                time.sleep(2)
                pswd_input.send_keys(Keys.ENTER)
                print("Duo Security")
                #Click Duo Auth button if not automatically enabled
                if onPage(driver, By.CLASS_NAME, "auth-button"):
                    time.sleep(3)
                    auth_button = driver.find_element(By.ID, "auth-button")
                    auth_button.click(By.CLASS_NAME, "auth-button")
                time.sleep(5)
            except NoSuchElementException:
                print("Login not found")

    def runBot(self):
        driver = webdriver.Chrome()
        driver.get("https://app.tophat.com/")
        refresh_counter = 0
        while True:
            try:
                time.sleep(5)
                # If there is an unanswered question, answer it
                if onPage(driver, By.CLASS_NAME, "list-row--unanswered"):
                    answerQuestion(driver)
                    pass
                elif driver.current_url == f"https://app.tophat.com/e/{self.class_code}/lecture/":
                    # Wait one minute and refresh the page
                    print("no question found...")
                    if refresh_counter > 30:
                        refresh_counter = 0
                        print("refreshing page")
                        driver.refresh()
                    refresh_counter += 1
                    pass
                # If on any stage of the login page, login to user account
                elif onPage(driver, By.ID, "select-input-1") or onPage(driver, By.NAME, "loginfmt") or onPage(driver, By.NAME, "passwd"):
                    self.login(driver)
                    print(f"logging in: {self.email}")
                    pass
                # If at home screen, open requested class
                elif driver.current_url == "https://app.tophat.com/e":
                    print(f"At homescreen: opening class {self.class_code}...")
                    driver.get(f"https://app.tophat.com/e/{self.class_code}")
                    pass
                else:
                    print("Nothing found")

            # If the browser was closed, quit the program
            except NoSuchWindowException:
                print("closing window...")
                driver.quit()
                break

    def runMultiBot(self):
        self.thread.start()


# jacob = Student("Pennsylvania State University (Penn State)", "jrm7250@psu.edu", "Ringgold819", "849492")
# bryan = Student("Pennsylvania State University (Penn State)", "bdn5122@psu.edu", "Ponies#5888", "849492")
# janel = Student("Pennsylvania State University (Penn State)", "jmn6017@psu.edu", "maryhadalittlelamb5", "849492")

# jacob.runMultiBot()
# bryan.runMultiBot()
# janel.runMultiBot()

# TESTING
test_jacob = Student("American Heritage University", "bryandn1210@gmail.com", "Ringgold819", "558410")
test_jacob.runMultiBot()
