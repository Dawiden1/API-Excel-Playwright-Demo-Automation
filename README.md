# API-Excel-Playwright-Demo-Automation

# Energy Automation Demo

**Energy Automation Demo** to pokazowa wersja rzeczywistej aplikacji automatyzującej przetwarzanie danych o nasłonecznieniu oraz generowanie raportów dla klientów z sektora energetycznego.  
Projekt ma na celu zaprezentowanie w CV umiejętności programistycznych, pracy z API, przetwarzania danych w Excelu, logowania do serwisów webowych (Playwright) oraz organizacji aplikacji w Pythonie.

---

## Cel projektu

Aplikacja automatyzuje codzienny proces:
1. Pobrania danych meteorologicznych z API (np. prognozy irradiancji słonecznej).
2. Przetworzenia danych i uzupełnienia szablonu Excela.
3. Zalogowania się do panelu operatora i przesłania gotowego raportu.
4. Rejestrowania pełnego logu procesu dla każdego klienta.

Wersja demo nie zawiera rzeczywistych danych klientów ani prawdziwych danych logowania – wszystkie dane są przykładowe, a komunikacja z API i stroną docelową jest symulowana.

---

## Technologie i biblioteki

| Zastosowanie                         | Technologia / biblioteka |
|-------------------------------------|--------------------------|
| Język                                | Python 3.10+             |
| Pobieranie danych                    | `requests`               |
| Przetwarzanie i generowanie Excela   | `openpyxl`               |
| Automatyzacja przeglądarki / upload  | `playwright`             |
| Logowanie i struktura logów          | `logging` (standard lib) |
| Harmonogram / CI                     | GitHub Actions           |

---

## 🗂️ Struktura projektu

energy-automation-demo/
│
├── main.py # Główny plik sterujący logiką aplikacji
├── irradiance.py # Komunikacja z API
├── excels.py # Generowanie i przetwarzanie plików Excel
├── pdk_energa.py # Logowanie i upload przez Playwright
│
├── clients/ # Przykładowe pliki JSON z klientami
│ └── demo_client.json
│
├── xlsx_files/ # Folder z szablonami i wynikowymi Excelami
│ └── NazwaFirmy/
│   ├── template.xlsx
│   └── YYYYMMDD_uzupelniony.xlsx
│
├── logs/ # Automatycznie tworzony katalog logów
│ └── YY_MM/
│   └── YY_MM_DD.log
│
├── requirements.txt
