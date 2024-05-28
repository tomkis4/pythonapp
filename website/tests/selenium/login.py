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




def test_login():

    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        driver.get("http://127.0.0.1:5000")
        time.sleep(3)

        # Strona Główna    ---------------------------

        login_button = driver.find_element(By.LINK_TEXT, "Zaloguj się")
        login_button.click()

        time.sleep(3)

        #teraz ustalamy gdzie driver ma szukać odpowiednich miejsc na stronie logowania
        

        username = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")
        button_click = driver.find_element(By.ID, "submit")

        # teraz driver będzie wypełniał pola

        username.send_keys("testuser123")
        password.send_keys("test1234")

        time.sleep(3)

        button_click.click()

        time.sleep(5)



    finally:

        driver.quit()

if __name__ == "__main__":
    test_login()