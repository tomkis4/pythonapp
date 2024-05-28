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
import pandas as pd
from colorama import Fore, Style
import traceback
import io

excel_file = 'data.xlsx'
results_file = 'wyniki_testów_rejestracji.txt'

def data_upload():
    df = pd.read_excel(excel_file)
    return df


def write_result(results, results_file):
    with io.open(results_file, 'w', encoding='utf8') as p:
        p.write("Podsumowanie wyników testów\n")

        for record in results:
            if record[2] == 'PASSED':
                p.write(f"Użytkownik: {record[0]}, Status: {record[2]}\n\n")
            else:
                p.write(f"Użytkownik: {record[0]}, Status: {record[2]}, Błąd: {record[3]}\n\n")


def test_register(login, password, results):

    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        driver.get("http://127.0.0.1:5000")
        time.sleep(1)

        # Strona Główna    --------------------------------------------------------------------------

        register_menu_button = driver.find_element(By.LINK_TEXT, "zarejestruj")
        register_menu_button.click()

        time.sleep(1)

        username1 = driver.find_element(By.ID, "username")
        password1 = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "submit")

        username1.send_keys(login)
        password1.send_keys(password)

        time.sleep(1)

        login_button.click()

        # Strona z logowaniem po rejestracji   ------------------------------------------------------

        time.sleep(1)
        driver.refresh()

        username2 = driver.find_element(By.ID, "username")
        pass2 = driver.find_element(By.ID, "password")
        login_button2 = driver.find_element(By.ID, "submit")

        username2.send_keys(login)
        pass2.send_keys(password)

        time.sleep(1)

        login_button2.click()

        # --------------------------------------------------------------------------------------------
        time.sleep(3)

        print(Fore.GREEN + f"PASSED: Rejestracja konta i logowanie dla użytkownika: {login} przebiegło pomyślnie." + Style.RESET_ALL)

        results.append((login, password, 'PASSED'))




    except:

        error_message = traceback.format_exc()
        print(Fore.RED + f"FAILED: Rejestracja nie przebiegła pomyślnie dla użytkownika: {login}. Błąd: {error_message}" + Style.RESET_ALL)

        results.append((login, password, 'FAILED', error_message))


    finally:
        driver.quit()

if __name__ == "__main__":

    data = data_upload()              # dane z df są przekazywane do dane
    results = []                         # w tej tablicy są tworzone wyniki do podsumowania pod koniec


    for index, row in data.iterrows():      # funkcja do iteracji po wierszach wewnątrz 'dane'
        login = row['login']
        password = row['password']
        print(f"Testowanie rejestracji dla użytkownika: {login} oraz hasła: {password}")
        test_register(login, password, results)


    print("\nPodsumowanie wyników testów:\n")     # Przechodzimy pętlą po tablicy wyniki i dopisujemy opis w oparciu o wynik
    for record in results:
        if record[2] == 'PASSED':
            print(Fore.GREEN + f"Użytkownik: {record[0]}, Status: {record[2]}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Użytkownik: {record[0]}, Status: {record[2]}, Błąd: {record[3]}" + Style.RESET_ALL)



    write_result(results, results_file)   # Nasza funkcja (druga) do zapisania wyniku w .txt
