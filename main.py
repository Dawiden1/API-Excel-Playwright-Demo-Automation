from irradiance import get_uv_forecast_hourly
from pdk_energa import pdk_login_and_upload
from excels import generate_excel
from datetime import datetime
import json
from glob import glob
from pathlib import Path
import logging
import os
import sys

# --- konfiguracja loggera ---
def setup_logger():
    year_month = datetime.today().strftime("%y_%m")
    year_month_day = datetime.today().strftime("%y%m_%d")

    log_dir = Path("logs") / year_month
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{year_month_day}.log"

    # utwórz logger główny
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # usuń stare handlery (żeby nie dublowało się przy wielokrotnym imporcie)
    logger.handlers.clear()

    # format logów
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # handler do pliku
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # handler do konsoli (w GitHub Actions będzie widoczny)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # log info o środowisku
    if os.getenv("GITHUB_ACTIONS"):
        logger.info("Running inside GitHub Actions environment.")
    else:
        logger.info("Running locally.")

    logger.info(f"Log file created at: {log_path}")
    return logger


logger = setup_logger()


# --- logika przetwarzania klientów ---
def process_client(client_path):
    with open(client_path, "r", encoding="utf-8") as f:
        client = json.load(f)

    city = client["additional"]["city"]
    company = client["company"]
    pdk_login = client["pdk_username"]
    pdk_password = client["pdk_password"]
    lat = client["lat"]
    lon = client["lon"]

    logger.info("-" * 70)
    logger.info(f"Processing client: {company} ({city})")

    try:
        json_file = get_uv_forecast_hourly(lat, lon)
        if not json_file:
            raise ValueError("Empty forecast data")
        logger.info(f"UV forecast retrieved successfully for {city}")
    except Exception as e:
        logger.exception(f"Error fetching UV forecast for {city}: {e}")
        return

    try:
        excel_file = generate_excel(json_file, company)
        logger.info(f"Excel file generated: {excel_file}")
    except Exception as e:
        logger.exception(f"Error generating Excel file for {city}: {e}")
        return

    try:
        pdk_login_and_upload(pdk_login, pdk_password, excel_file)
        logger.info(f"Excel file uploaded successfully for {company}")
    except Exception as e:
        logger.exception(f"Error uploading Excel file for {company}: {e}")
        return


def main():
    client_files = glob("clients/*.json")

    if not client_files:
        logger.warning("No client JSON files found in ./clients directory.")
        return

    logger.info(f"Found {len(client_files)} client(s) to process.")
    for client_file in client_files:
        process_client(client_file)

    logger.info("All clients processed. Script finished.")


if __name__ == "__main__":
    main()
