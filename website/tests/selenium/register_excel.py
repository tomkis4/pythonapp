from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from colorama import Fore, Style
import traceback
import io

plik_excel = 'data.xlsx'
plik_wyniki = 'wyniki_testów_rejestracji.txt'

def odczyt_danych():
    df = pd.read_excel(plik_excel)
    return df


def zapisanie_wyniku(wyniki, plik_wyniki):
    with io.open(plik_wyniki, 'w', encoding='utf8') as p:
        p.write("Podsumowanie wyników testów\n")

        for record in wyniki:
            if record[2] == 'PASSED':
                p.write(f"Użytkownik: {record[0]}, Status: {record[2]}\n\n")
            else:
                p.write(f"Użytkownik: {record[0]}, Status: {record[2]}, Błąd: {record[3]}\n\n")


def test_rejestracja(login, password, wyniki):

    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        driver.get("http://127.0.0.1:5000")
        time.sleep(1)

        # Strona Główna    --------------------------------------------------------------------------

        przycisk_do_logowania = driver.find_element(By.LINK_TEXT, "zarejestruj")
        przycisk_do_logowania.click()

        time.sleep(1)

        nazwa_uzytkownika = driver.find_element(By.ID, "username")
        haslo = driver.find_element(By.ID, "password")
        przycisk_zaloguj = driver.find_element(By.ID, "submit")

        nazwa_uzytkownika.send_keys(login)
        haslo.send_keys(password)

        time.sleep(1)

        przycisk_zaloguj.click()

        # Strona z logowaniem po rejestracji   ------------------------------------------------------

        time.sleep(1)
        driver.refresh()

        nazwa_uzytkownika2 = driver.find_element(By.ID, "username")
        haslo2 = driver.find_element(By.ID, "password")
        przycisk_zaloguj2 = driver.find_element(By.ID, "submit")

        nazwa_uzytkownika2.send_keys(login)
        haslo2.send_keys(password)

        time.sleep(1)

        przycisk_zaloguj2.click()

        # --------------------------------------------------------------------------------------------
        time.sleep(3)

        print(Fore.GREEN + f"PASSED: Rejestracja konta i logowanie dla użytkownika: {login} przebiegło pomyślnie." + Style.RESET_ALL)

        wyniki.append((login, password, 'PASSED'))




    except:

        error_message = traceback.format_exc()
        print(Fore.RED + f"FAILED: Rejestracja nie przebiegła pomyślnie dla użytkownika: {login}. Błąd: {error_message}" + Style.RESET_ALL)

        wyniki.append((login, password, 'FAILED', error_message))


    finally:
        driver.quit()

if __name__ == "__main__":
    dane = odczyt_danych()              # dane z df są przekazywane do dane

    wyniki = []                         # w tej tablicy są tworzone wyniki do podsumowania pod koniec


    for index, kolumna in dane.iterrows():      # funkcja do iteracji po wierszach wewnątrz 'dane'
        login = kolumna['login']
        password = kolumna['password']
        print(f"Testowanie rejestracji dla użytkownika: {login} oraz hasła: {password}")
        test_rejestracja(login, password, wyniki)


    print("\nPodsumowanie wyników testów:\n")     # Przechodzimy pętlą po tablicy wyniki i dopisujemy opis w oparciu o wynik
    for record in wyniki:
        if record[2] == 'PASSED':
            print(Fore.GREEN + f"Użytkownik: {record[0]}, Status: {record[2]}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Użytkownik: {record[0]}, Status: {record[2]}, Błąd: {record[3]}" + Style.RESET_ALL)



    zapisanie_wyniku(wyniki, plik_wyniki)   # Nasza funkcja (druga) do zapisania wyniku w .txt
