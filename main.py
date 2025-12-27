from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import json, os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
bot_token = os.getenv("BOT_TOKEN")

# This function is for getting a provided crypto's data such as price, market cap, volume and more
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

# This function is for getting top 10 crypto data at the current time
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

# Telegram command to start this bot
async def start_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	message = "Hey, welcome to Crypto Bot. I can give the real time data for any cryptocurrency. Use /crypto <token-name> to start."
	await update.message.reply_text(message)

# Telegram command to get the data of a crypto token
# returns these data about a token: (Price, 24h change price and percentage, 24h lowest and highest price, market cap, total volume, total supply, circulating supply)
async def crypto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	crypto_name = update.message.text.split()[1]
	crypto_data = get_crypto_price(crypto_name)
	if crypto_data:
		await update.message.reply_text(f"The current price of {crypto_name} is ${crypto_data['current_price']}.\nThe price change in last 24h: ${crypto_data['price_change_24h']} | %{crypto_data['price_change_percentage_24h']}\nLowest in the last 24h: ${crypto_data['low_24h']}\nHighest in the last 24h: ${crypto_data['high_24h']}\nMarket cap: ${crypto_data['market_cap']}\nLast 24h total volume: ${crypto_data['total_volume']}\nTotal supply: {crypto_data['total_supply']}\nCirculating supply: {crypto_data['circulating_supply']}")
	else:
		await update.message.reply_text(f"Sorry, I could not get any available data for {crypto_name}. Please check the token name and try again.")

# Telegram command to get top 10 crypto
async def top_cryptocurrencies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	data = get_top_cryptos()
	if data:
		message = 'Here is the top 10 cryptocurrencies:\n'
		for number, token in enumerate(data, start=1):
			message += f"{number}. [{token['name']}] ( {token['symbol'].upper()} ):\n- Current price: ${token['current_price']}\n- Market cap: ${token['market_cap']}\n- Total volume in last 24h: ${token['total_volume']}\n\n"
		await update.message.reply_text(message, parse_mode='Markdown')
	else:
		await update.message.reply_text(f"Sorry, I could not get any available data for top 10 cryptocurrency. Try again later.")

app = ApplicationBuilder().token(bot_token).build()

app.add_handler(CommandHandler('Start', start_bot))
app.add_handler(CommandHandler('Crypto', crypto))
app.add_handler(CommandHandler('Top', top_cryptocurrencies))

app.run_polling()