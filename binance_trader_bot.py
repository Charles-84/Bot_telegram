import json
import logging
from pathlib import Path

import requests
from colorama import Fore
from telegram import Update
from telegram.ext import CallbackContext

from Binance.Analyse import analyse_binance
from trader_info import TraderInfo

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger_fonction = logging.getLogger('SCRAP')
logger_fonction.setLevel(logging.INFO)
handler = logging.FileHandler(filename=Path("LOG", "scrap.log"), encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger_fonction.addHandler(handler)

class BinanceTraderBot:
    def __init__(self):
        pass

    def fetch_trader_data(self, update: Update, context: CallbackContext):
        
        json_data = {
                'encryptedUid': "3AFFCB67ED4F1D1D8437BA17F4E8E5ED",
                'tradeType': 'PERPETUAL',
            }
        
        url = "https://www.binance.com/bapi/futures/v1/public/future/leaderboard/getOtherPosition"
        response = requests.post(url, json=json_data)
        if response.status_code == 200:
            data = response.json()
            type, ID_name, timestamp, symbol,position, amount, levred, entry_price = analyse_binance.analyze_Binance_C_M(self,order=data,ID='516CDC807D6DFC13263169A91C83B2FD', ID_name="sacaloco", update=update, context=context)

            analyse_binance.message_binance(type, ID_name, timestamp, symbol,position, amount, levred, entry_price, update=update, context=context)
        else:
            logging.warning(f"Failed to fetch trader data. Status code: {response.status_code}")

    def fetch_top_trader_data(self):
        url = "https://www.binance.com/bapi/futures/v3/public/future/leaderboard/getLeaderboardRank"
        
        payload = {"tradeType":"PERPETUAL","statisticsType":"ROI","periodType":"ALL","isShared":True,"isTrader":False}
        
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        if response.status_code == 200:
            top_traders_data = response.json()
            traders = top_traders_data.get('data', [])
            traders_sorted = sorted(traders,key=lambda x: x['rank'])
            return traders_sorted
    
    def fetch_detailed_stats(encrypted_uid):
        url = "https://www.binance.com/bapi/futures/v2/public/future/leaderboard/getOtherPerformance"
        payload = {"encryptedUid": encrypted_uid, "tradeType": "PERPETUAL"}
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None

