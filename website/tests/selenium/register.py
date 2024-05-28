from selenium import webdriver
from selenium.webdriver.common.by import By
import time




def test_rejestracja():

    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        driver.get("http://127.0.0.1:5000")
        time.sleep(3)

        # Strona Główna    ---------------------------

        przycisk_do_logowania = driver.find_element(By.LINK_TEXT, "zarejestruj")
        przycisk_do_logowania.click()

        time.sleep(2)

        nazwa_uzytkownika = driver.find_element(By.ID, "username")
        haslo = driver.find_element(By.ID, "password")
        przycisk_zaloguj = driver.find_element(By.ID, "submit")

        nazwa_uzytkownika.send_keys("test5")
        haslo.send_keys("test12345")

        time.sleep(2)

        przycisk_zaloguj.click()

        time.sleep(2)
        driver.refresh()

        nazwa_uzytkownika2 = driver.find_element(By.ID, "username")
        haslo2 = driver.find_element(By.ID, "password")
        przycisk_zaloguj2 = driver.find_element(By.ID, "submit")

        nazwa_uzytkownika2.send_keys("test5")
        haslo2.send_keys("test12345")

        time.sleep(2)

        przycisk_zaloguj2.click()

        time.sleep(4)




    finally:

        driver.quit()

if __name__ == "__main__":
    test_rejestracja()



