"""
This file is part of the CatsApp.

Authors:
- Julia Herold
- Tomasz Kiselyczka
- Grzegorz Szymanik

Licensed under the MIT License. See LICENSE file in the project root for full license information.
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
import time




def test_register():

    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        driver.get("http://127.0.0.1:5000")
        time.sleep(3)

        # Strona Główna    ---------------------------

        menu_button_login = driver.find_element(By.LINK_TEXT, "zarejestruj")
        menu_button_login.click()

        time.sleep(2)

        username1 = driver.find_element(By.ID, "username")
        username2 = driver.find_element(By.ID, "username")
        pass1 = driver.find_element(By.ID, "password")
        pass2 = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "submit")
        login_button2 = driver.find_element(By.ID, "submit")


        username1.send_keys("testuser9")
        pass1.send_keys("test1234")

        time.sleep(2)

        login_button.click()

        time.sleep(2)

        username2.send_keys("testuser9")
        pass2.send_keys("test1234")

        time.sleep(2)

        login_button2.click()




    finally:

        driver.quit()

if __name__ == "__main__":
    test_register()



