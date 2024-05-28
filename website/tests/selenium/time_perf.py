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

results_file= 'wyniki_wydajnosci.txt'

def meter(driver, url):
    start_time = time.time()
    driver.get(url)
    end_time = time.time()
    return end_time - start_time

def perf_test():

    driver = webdriver.Chrome()
    driver.maximize_window()
    results = []

    try:
        time_main= meter(driver, "http://127.0.0.1:5000")
        print(f"Czas ładowania strony głównej: {time_main:.2f} sekund")
        results.append(("Strona główna", time_main))

        time_register= meter(driver, "http://127.0.0.1:5000/register")
        print(f"Czas ładowania strony rejestracji: {time_register:.2f} sekund")
        results.append(("Strona rejestracji", time_register))

    finally:

        driver.quit()

    return results

def write_results_file(results, results_file):
    with io.open(results_file, 'w', encoding='utf8') as f:

        f.write("Podsumowanie wyników testów wydajności:\n")

        for result in results:
            f.write(f"{result[0]}, Czas ładowania: {result[1]:.2f} sekund\n")



if __name__ == "__main__":

    results = perf_test()

    print("\nPodsumowanie wyników testów wydajności:")
    for result in results:
         print(f"{result[0]}, Czas ładowania: {result[1]:.2f} sekund")



    write_results_file(results, results_file)    # Zapisanie wyników do pliku .txt
