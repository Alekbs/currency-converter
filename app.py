from flask import Flask, render_template, request, jsonify
from  models.models import db, ExchangeRate
from utils.fetch_rates import fetch_and_save_rates, get_last_updated
from dotenv import load_dotenv
from threading import Thread
from time import sleep


load_dotenv()

app = Flask(__name__)
db.connect()


def update_rates_background():
    while True:
        try:
            fetch_and_save_rates()
            print("Курсы обновлены")
        except Exception as e:
            print(f"[ОШИБКА обновления курсов]: {e}")
        sleep(5)

# @app.before_request
def activate_background_updater():
    Thread(target=update_rates_background, daemon=True).start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/update-rates")
def update_rates():
    fetch_and_save_rates()
    return "Курсы обновлены"

@app.route("/last-update")
def last_update():
    return jsonify({"last_update": get_last_updated()})

@app.route('/convert', methods=['POST'])
def convert_currency():
    try:
        # Получаем данные из запроса
        data = request.get_json()
        from_currency = data.get('from')
        to_currency = data.get('to')
        amount = data.get('amount')

        # Проверяем, что все данные присутствуют
        if not all([from_currency, to_currency, amount]):
            return jsonify({"error": "Missing required parameters"}), 400

        try:
            amount = float(amount)
        except ValueError:
            return jsonify({"error": "Invalid amount"}), 400

        # Получаем курсы валют из базы данных
        try:
            from_rate = ExchangeRate.get(ExchangeRate.currency == from_currency).rate
            to_rate = ExchangeRate.get(ExchangeRate.currency == to_currency).rate
        except ExchangeRate.DoesNotExist:
            return jsonify({"error": f"Currency {from_currency} or {to_currency} not found in database"}), 404

        # Выполняем конвертацию
        result = (amount / from_rate) * to_rate

        # Возвращаем результат
        return jsonify({"result": round(result, 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400
@app.route('/currencies', methods=['GET'])
def get_currencies():
    try:
        # Получаем все валюты из базы данных
        currencies = ExchangeRate.select(ExchangeRate.currency).distinct()
        currency_list = [currency.currency for currency in currencies]
        
        # Возвращаем список валют в формате JSON
        return jsonify({"currencies": currency_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
