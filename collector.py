import json
import ssl
import urllib.parse
import urllib.request
import certifi
import psycopg2
import logging
from dotenv import load_dotenv
load_dotenv()
import os

logging.basicConfig(
	filename = "logs/crypto_tracker.log",
	level = logging.INFO,
	format = "%(asctime)s | %(levelname)s | %(message)s",
	datefmt = "%Y-%m-%d %H:%M:%S"
	)

logging.info("=========Starting Collection=========")

try:
	conn = psycopg2.connect(dbname= os.getenv("DB_NAME"),
			user= os.getenv("DB_USER"),
			password = os.getenv("DB_PASSWORD"),
			host= os.getenv("DB_HOST"),
			port = os.getenv("DB_PORT"))
	cur = conn.cursor()
	print("connection to crypto_tracker_DB was successfull")
	logging.info("connection to DB was successfull!")
except Exception as e:
	print(e)
	logging.info(e)


params = urllib.parse.urlencode(
    {
        "start": "1",
        "limit": "100",
        "convert": "USD",
    })

try:
	request = urllib.request.Request(
    f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?{params}",
    headers={
        "Accept": "application/json",
        "X-CMC_PRO_API_KEY": os.getenv("CMC_API_KEY"),
    		}
	                                )

	context = ssl.create_default_context(cafile=certifi.where())

	with urllib.request.urlopen(request, context=context) as response:
		data = json.load(response)
	logging.info("retrieved 100 coins")
	print('retrieved 100 coins')
except Exception as e:
	print(e)
	logging.error(f"API error: {e}")
	logging.info("=========Collection Closed=========")
	exit()

try:
	for coin in data["data"]:
		cur.execute("""
					INSERT INTO coins (
										coin_id,
										symbol,
										name,
										slug,
										date_added,
										max_supply,
										infinite_supply
										)
					VALUES (%s,%s,%s,%s,%s,%s,%s)
					ON CONFLICT (coin_id) DO NOTHING""",
					(
										coin["id"],
										coin["symbol"],
										coin["name"],
										coin["slug"],
										coin["date_added"],
										coin["max_supply"],
										coin["infinite_supply"]
					)
					)

		cur.execute("""
					INSERT INTO price_snapshots(
												coin_id,
												collected_at,
												price_usd,
												market_cap,
												volume_24h,
												circulating_supply,
												cmc_rank
												)
					VALUES (%s,%s,%s,%s,%s,%s,%s)
					""",
					(
												coin["id"],
												coin["last_updated"],
												coin["quote"]["USD"]["price"],
												coin["quote"]["USD"]["market_cap"],
												coin["quote"]["USD"]["volume_24h"],
												coin["circulating_supply"],
												coin["cmc_rank"]
					)
					)
	print('100 data inserted to db')
	logging.info('inserted 100 snapshots')
except Exception as e:
	conn.rollback()
	print(e)
	logging.info(e)

conn.commit()
logging.info("=========Collection Complete=========")
