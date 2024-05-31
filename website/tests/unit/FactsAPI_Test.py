import requests
import traceback
import io

plik_wynikowy = 'wyniki_testu_api_cat_facts.txt'

def test_cat_facts_api():
    wynik_testu = {"test": "Cat Facts API", "result": None, "error": None, "fact": None}
    try:
        response = requests.get('https://catfact.ninja/fact')
        if response.status_code == 200:
            data = response.json()
            fact = data.get('fact', None)
            if fact:
                wynik_testu["result"] = "PASSED"
                wynik_testu["fact"] = fact
            else:
                wynik_testu["result"] = "FAILED"
                wynik_testu["error"] = "Nie otrzmano faktu od zewnętrzengo API"
        else:
            wynik_testu["result"] = "FAILED"
            wynik_testu["error"] = f"Response status code: {response.status_code}"

    except Exception as e:
        wynik_testu["result"] = "FAILED"
        wynik_testu["error"] = traceback.format_exc()

    return wynik_testu

def zapisanie(wyniki, plik_wynikowy):
    with io.open(plik_wynikowy, 'a', encoding="utf8") as f:
        f.write("\nPodsumowanie wyników testów API:\n")
        for wynik in wyniki:
            f.write(f"Test: {wynik['test']}, Wynik: {wynik['result']}\n")
            if wynik["fact"]:
                f.write(f"Fact: {wynik['fact']}\n")
            if wynik["error"]:
                f.write(f"Błąd: {wynik['error']}\n")

if __name__ == "__main__":
    wyniki = []
    wynik_testu = test_cat_facts_api()
    wyniki.append(wynik_testu)

    zapisanie(wyniki, plik_wynikowy)

    print("\n\nPodsumowanie wyników testów API:")
    for wynik in wyniki:
        print(f"Test: {wynik['test']}, Wynik: {wynik['result']}")
        if wynik["fact"]:
            print(f"Fact: {wynik['fact']}")
        if wynik["error"]:
            print(f"Błąd: {wynik['error']}")

#