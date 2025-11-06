from playwright.sync_api import sync_playwright
import logging
logger = logging.getLogger(__name__)

def pdk_login_and_upload (USERNAME, PASSWORD, EXCEL_FILE):
    with sync_playwright() as p:
        LOGIN_URL = "https://pdk.energa-operator.pl/PDK2/login"
        GEN_URL = "https://pdk.energa-operator.pl/PDK2/generations"

        logger.info("Running chromium sesion")
        browser = p.chromium.launch(headless=True)  # headless=True jeśli ma działać w tle
        page = browser.new_page()

        # Otworzenie strony logowania
        logger.info("Going to login page")
        page.goto(LOGIN_URL)
        page.wait_for_timeout(2000)

        # Wpisanie loginu i hasła
        logger.info("Filling username & password")
        page.fill("input[placeholder*='Adres e-mail']", USERNAME)
        page.fill("input[type='password']", PASSWORD)
        page.wait_for_timeout(1000)

        # Klik przycisku "Zaloguj się"
        logger.info("Logging in")
        page.click("button:has-text('Zaloguj się')")
        page.wait_for_timeout(2000)

        if page.locator("div.alert.alert-danger[role='alert']").is_visible():
            raise ValueError("Login failed: invalid username or password")
            return

        # Przejscie do zakładki generations
        logger.info("Going to generation page")
        page.goto(GEN_URL)
        page.wait_for_timeout(2000)

        # Ikona "Upload" i wybranie opcji "Import z pliku Excel"
        logger.info("Beginning of sending the Excel file")
        page.click("#sendIcon")
        page.click("text=Import z pliku Excel")
        page.wait_for_timeout(2000)

        # W modalu wybierz plik (ukryty input file)
        logger.info("Uploading the Excel file")
        page.set_input_files("input#uploadFile", EXCEL_FILE)
        page.wait_for_timeout(5000)

        # Klikanie przycisku "Ok"
        logger.info("Confirming the upload")
        page.click("div.modal-content >> text=Ok")

        # Poczekaj na potwierdzenie importu
        page.wait_for_timeout(2000)
        browser.close()
