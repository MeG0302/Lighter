# bot.py
import os
import time
from dotenv import load_dotenv
from lighter_client import LighterBot

load_dotenv()

# Load private keys
PRIVATE_KEY_1 = os.getenv("PRIVATE_KEY_1")
PRIVATE_KEY_2 = os.getenv("PRIVATE_KEY_2")

# Initialize bots
bot1 = LighterBot(PRIVATE_KEY_1)  # LONG bot
bot2 = LighterBot(PRIVATE_KEY_2)  # SHORT bot

def run_trade_cycle(interval_minutes=2, symbol="ETH-PERP", size=0.01):
    try:
        print(f"Placing trades... (interval: {interval_minutes} minutes)")
        bot1.place_market_order(symbol, "buy", size)  # LONG
        bot2.place_market_order(symbol, "sell", size) # SHORT

        print(f"Sleeping for {interval_minutes} minutes...")
        time.sleep(interval_minutes * 60)

        print("Closing trades...")
        bot1.close_all_positions()
        bot2.close_all_positions()
        print("Cycle completed.\n")

    except Exception as e:
        print(f"❌ Error during trade cycle: {str(e)}")
