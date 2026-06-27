SOURCE_ID = 1 #CoinMarketCap
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
from datetime import datetime

def insert_coin_info(curser, coin):
	curser.execute("""
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


def insert_full_snapshot(curser, coin, source_id):
	curser.execute("""
					INSERT INTO market_snapshots(
												coin_id,
												source_updated_at,
												price_usd,
												market_cap,
												volume_24h,
												circulating_supply,
												cmc_rank,
												fully_diluted_market_cap,
			 									volume_change_24h,
			 									market_cap_dominance,
			 									precent_change_1h,
												precent_change_24h,
												precent_change_7d,
			 									precent_change_30d,
			 									tvl,
			 									tvl_ratio,
			 									cex_volume_24h,
			 									dex_volume_24h,
												source_id			 
												)
					VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
					""",
					(
					coin["id"],
					coin["last_updated"],
					coin["quote"]["USD"]["price"],
					coin["quote"]["USD"]["market_cap"],
					coin["quote"]["USD"]["volume_24h"],
					coin["circulating_supply"],
					coin["cmc_rank"],
					coin["quote"]["USD"]["fully_diluted_market_cap"],
					coin["quote"]["USD"]["volume_change_24h"],
					coin["quote"]["USD"]["market_cap_dominance"],
					coin["quote"]["USD"]["percent_change_1h"],
					coin["quote"]["USD"]["percent_change_24h"],
					coin["quote"]["USD"]["percent_change_7d"],
					coin["quote"]["USD"]["percent_change_30d"],
					coin["quote"]["USD"]["tvl"],
					coin["tvl_ratio"],
					coin["quote"]["USD"]["cex_volume_24h"],
					coin["quote"]["USD"]["dex_volume_24h"],
					SOURCE_ID
					)
					)


def insert_medium_snapshots(curser,coin,source_id):
	curser.execute("""
					INSERT INTO market_snapshots(
												coin_id,
												source_updated_at,
												price_usd,
												market_cap,
												volume_24h,
												circulating_supply,
												cmc_rank,
												source_id			 
												)
					VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
					""",
					(
					coin["id"],
					coin["last_updated"],
					coin["quote"]["USD"]["price"],
					coin["quote"]["USD"]["market_cap"],
					coin["quote"]["USD"]["volume_24h"],
					coin["circulating_supply"],
					coin["cmc_rank"],
					SOURCE_ID
					)
					)
	

def insert_light_snapshot(curser,coin,source_id):
	cur.execute("""
					INSERT INTO market_snapshots(
												coin_id,
												source_updated_at,
												price_usd,
												market_cap,
												cmc_rank,
												source_id	 
												)
					VALUES (%s,%s,%s,%s,%s,%s)
					""",
					(
					coin["id"],
					coin["last_updated"],
					coin["quote"]["USD"]["price"],
					coin["quote"]["USD"]["market_cap"],
					coin["cmc_rank"],
					SOURCE_ID
					)
					)


logging.basicConfig(
	filename = "logs/crypto_tracker.log",
	level = logging.INFO,
	format = "%(asctime)s | %(levelname)s | %(message)s",
	datefmt = "%Y-%m-%d %H:%M:%S"
	)

logging.info("=========Starting Collection=========")
start_time = datetime.now()
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
        "limit": "400",
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
	logging.info(f"retrieved {len(data['data'])} coins from json")
	print(f"retrieved {len(data['data'])} coins")
except Exception as e:
	print(e)
	logging.error(f"API error: {e}")
	logging.info("=========Collection Closed=========")
	exit()


try:
	for coin in data["data"]:
		rank = coin['cmc_rank']
		insert_coin_info(cur,coin)
		
		if rank <= 100:
			insert_full_snapshot(cur,coin,SOURCE_ID)

		elif rank <= 200:
			insert_medium_snapshots(cur,coin,SOURCE_ID)

		elif rank <= 400:
			insert_light_snapshot(cur,coin,SOURCE_ID)
		

		#insert market_snapshots here
		
	print('data inserted to db')
	logging.info(f'inserted {len(data['data'])} coins snapshots.')
except Exception as e:
	conn.rollback()
	print(e)
	logging.info(e)

conn.commit()
end_time = datetime.now()
logging.info(f"collector finished. duration: {end_time - start_time}")
logging.info("=========Collection Complete=========")
