from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import json, os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

def get_crypto_price(crypto):
	try:
		url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={crypto}&api_key={api_key}"
		response = requests.get(url)
		response.raise_for_status()
		data = response.json()[0]
		return data
	except requests.exceptions.HTTPError as errh:
		print("Http Error:", errh)
	except requests.exceptions.ConnectionError as errc:
		print("Error Connecting:", errc)
	except requests.exceptions.Timeout as errt:
		print("Timeout Error:", errt)
	except requests.exceptions.RequestException as err:
		print("Something went wrong:", err)

def get_top_cryptos():
	try:
		url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false&api_key={api_key}"
		response = requests.get(url)
		response.raise_for_status()
		data = response.json()
		return data
	except requests.exceptions.HTTPError as errh:
		print("Http Error:", errh)
	except requests.exceptions.ConnectionError as errc:
		print("Error Connecting:", errc)
	except requests.exceptions.Timeout as errt:
		print("Timeout Error:", errt)
	except requests.exceptions.RequestException as err:
		print("Something went wrong:", err)
