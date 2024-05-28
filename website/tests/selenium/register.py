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

        login_menu_button = driver.find_element(By.LINK_TEXT, "zarejestruj")
        login_menu_button.click()

        time.sleep(2)

        username = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "submit")

        username.send_keys("test5")
        password.send_keys("test12345")

        time.sleep(2)

        login_button.click()

        time.sleep(2)
        driver.refresh()

        username2 = driver.find_element(By.ID, "username")
        password2 = driver.find_element(By.ID, "password")
        login_button2 = driver.find_element(By.ID, "submit")

        username2.send_keys("test5")
        password2.send_keys("test12345")

        time.sleep(2)

        login_button2.click()

        time.sleep(4)




    finally:

        driver.quit()

if __name__ == "__main__":
    test_register()



