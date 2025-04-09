import requests
from datetime import datetime
from models.models import ExchangeRate, db
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("EXCHANGE_API_KEY")
BASE_CURRENCY = "USD"

API_URL = f"https://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}"


def fetch_and_save_rates():
    try:
        response = requests.get(API_URL)
        data = response.json()

        if "error" in data:
            print("[API ERROR]", data["error"])
            return

        rates = data.get("rates", {})
        now = datetime.now()

        with db.atomic():
            ExchangeRate.delete().execute()
            for currency, rate in rates.items():
                ExchangeRate.create(currency=currency, rate=rate, updated_at=now)

        print("Курсы успешно обновлены", now)

    except Exception as e:
        print("[ОШИБКА ПРИ ЗАПРОСЕ]", e)


def get_last_updated():
    rate = ExchangeRate.select().order_by(ExchangeRate.updated_at.desc()).first()
    return rate.updated_at.strftime("%Y-%m-%d %H:%M:%S") if rate else "Нет данных"
