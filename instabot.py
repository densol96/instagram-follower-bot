from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import os
import time


class InstagramFollowerBot:
    INSTAGRAM_USERNAME = os.getenv("INSTA_NAME")
    INSTAGRAM_PASSWORD = os.getenv("INSTA_PSWD")

    def __init__(self):
        chrome_driver_path = ChromeDriverManager().install()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        service = ChromeService(executable_path=chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        # self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.login(self.driver)

    def login(self, driver):
        driver.get("https://www.instagram.com/")
        time.sleep(2)
        allow_cookies = driver.find_element(
            By.XPATH,
            "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]",
        )
        allow_cookies.click()
        username_form = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
        password_form = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        username_form.send_keys(InstagramFollowerBot.INSTAGRAM_USERNAME)
        password_form.send_keys(InstagramFollowerBot.INSTAGRAM_PASSWORD + Keys.ENTER)
        time.sleep(5)
        self.follow(self.driver)

    def follow(self, driver):
        account_name = input("What's the name of account you are looking for? ")
        amount_to_follow = int(input("How many people would you like to follow? "))
        driver.get(f"https://www.instagram.com/{account_name}/followers/")
        folowers_container = driver.find_element(By.CSS_SELECTOR, "div._aano")
        time.sleep(2)

        while True:
            # Need to scroll down to make button elements appear in the DOM
            driver.execute_script("arguments[0].scrollTop += 300;", folowers_container)
            time.sleep(0.5)
            to_follow_buttons = driver.find_elements(By.CSS_SELECTOR, "button._acan")[
                1::
            ]
            # +1 in case you yourself is one of the followers
            if len(to_follow_buttons) + 1 >= amount_to_follow:
                break

        time.sleep(1)
        # Scroll back up to start from the 1st button element
        driver.execute_script("arguments[0].scrollIntoView();", to_follow_buttons[0])
        time.sleep(2)
        counter = 0
        for button in to_follow_buttons:
            btn_text = button.find_element(By.CSS_SELECTOR, "div[dir='auto']").text
            if btn_text == "Following" or btn_text == "Requested":
                print("You already followed this account!")
                continue

            try:
                button.click()
            except:
                pass
            else:
                counter += 1

            if counter == amount_to_follow:
                break
            time.sleep(1.5)

        print(f"{counter} people followed!")
