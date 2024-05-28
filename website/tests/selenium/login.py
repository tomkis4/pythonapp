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




def test_logowanie():

    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        driver.get("http://127.0.0.1:5000")
        time.sleep(3)

        # Strona Główna    ---------------------------

        przycisk_do_logowania = driver.find_element(By.LINK_TEXT, "Zaloguj się")
        przycisk_do_logowania.click()

        time.sleep(3)

        #teraz ustalamy gdzie driver ma szukać odpowiednich miejsc na stronie logowania
        #----------------------------------------------------------------------------------

        nazwa_uzytkownika = driver.find_element(By.ID, "username")
        haslo = driver.find_element(By.ID, "password")
        przycisk_zaloguj = driver.find_element(By.ID, "submit")

        # teraz driver będzie wypełniał pola

        nazwa_uzytkownika.send_keys("cebula123")
        haslo.send_keys("greg1234")

        time.sleep(3)

        przycisk_zaloguj.click()

        time.sleep(5)



    finally:

        driver.quit()

if __name__ == "__main__":
    test_logowanie()