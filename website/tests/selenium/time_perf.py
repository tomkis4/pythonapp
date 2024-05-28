"""
This file is part of the CatsApp.

Authors:
- Julia Herold
- Tomasz Kiselyczka
- Grzegorz Szymanik

Licensed under the MIT License. See LICENSE file in the project root for full license information.
"""


from selenium import webdriver
import time
import io

plik_z_czasami= 'wyniki_wydajnosci.txt'

def pomiar(driver, url):
    start_time = time.time()
    driver.get(url)
    end_time = time.time()
    return end_time - start_time

def test_wydajnosci():

    driver = webdriver.Chrome()
    driver.maximize_window()
    wyniki = []

    try:
        czas_main= pomiar(driver, "http://127.0.0.1:5000")
        print(f"Czas ładowania strony głównej: {czas_main:.2f} sekund")
        wyniki.append(("Strona główna", czas_main))

        czas_register= pomiar(driver, "http://127.0.0.1:5000/register")
        print(f"Czas ładowania strony rejestracji: {czas_register:.2f} sekund")
        wyniki.append(("Strona rejestracji", czas_register))

    finally:

        driver.quit()

    return wyniki

def zapisz_wyniki_do_pliku(wyniki, plik_wynikowy):
    with io.open(plik_wynikowy, 'w', encoding='utf8') as f:

        f.write("Podsumowanie wyników testów wydajności:\n")

        for wynik in wyniki:
            f.write(f"{wynik[0]}, Czas ładowania: {wynik[1]:.2f} sekund\n")



if __name__ == "__main__":

    wyniki = test_wydajnosci()

    print("\nPodsumowanie wyników testów wydajności:")
    for wynik in wyniki:
         print(f"{wynik[0]}, Czas ładowania: {wynik[1]:.2f} sekund")



    zapisz_wyniki_do_pliku(wyniki, plik_z_czasami)    # Zapisanie wyników do pliku .txt
