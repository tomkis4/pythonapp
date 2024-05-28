from selenium import webdriver
from selenium.webdriver.common.by import By
import time




def test_navigation():
    driver = webdriver.Chrome()
    driver.maximize_window()


    try:
        driver.get("http://127.0.0.1:5000/")        #Wchodzimy na stronę główną
        time.sleep(2)


        register_button = driver.find_element(By.LINK_TEXT, "Zaloguj się")
        register_button.click()
        time.sleep(2)

        # Wchodzimy do panelu logowania

        username1 = driver.find_element(By.ID, "username")
        password1 = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "submit")

        username1.send_keys("przyklad123")
        password1.send_keys("test1234")

        time.sleep(3)

        login_button.click()

        time.sleep(3)

        # Wchodzimy na obrazy z kotami

        cats_image_button = driver.find_element(By.LINK_TEXT, "Zobacz koty")
        cats_image_button.click()

        time.sleep(3)

        # Klik w kolejny obrazek

        cats_image_next_button = driver.find_element(By.ID, "nextButton")

        cats_image_next_button.click()
        time.sleep(3)

        cats_image_next_button.click()
        time.sleep(3)

        cats_image_next_button.click()
        time.sleep(3)

        driver.back()
        time.sleep(3)

        forum_button = driver.find_element(By.LINK_TEXT, "Forum")
        forum_button.click()

        time.sleep(3)

        forum_add_button = driver.find_element(By.LINK_TEXT, "Dodaj nowy post")
        forum_add_button.click()

        time.sleep(3)

        # Tu dodajemy dane do postu

        title = driver.find_element(By.ID, "post_title")
        text = driver.find_element(By.ID, "post_content")
        login_button2 = driver.find_element(By.ID, "submit")

        title.send_keys("Nowy przykladowy test1")
        text.send_keys("test test test test")

        time.sleep(3)

        login_button2.click()

        time.sleep(5)

        facts_button = driver.find_element(By.LINK_TEXT, "Losowe fakty o kotach")
        facts_button.click()

        time.sleep(3)

        cats_facts_next_button = driver.find_element(By.ID, "nextFactButton")
        cats_facts_next_button.click()

        time.sleep(3)
        cats_facts_next_button.click()

        time.sleep(3)
        cats_facts_next_button.click()

        time.sleep(3)
        cats_facts_next_button.click()

        time.sleep(3)
        driver.back()

        time.sleep(3)

        policy_button = driver.find_element(By.LINK_TEXT, "Polityka prywatności")
        policy_button.click()

        time.sleep(6)










    finally:
        driver.quit()




if __name__ == "__main__":

    test_navigation()





