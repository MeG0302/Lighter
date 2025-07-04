# lighter_client.py
import os
from lighter import LighterClient
from dotenv import load_dotenv

load_dotenv()

class LighterBot:
    def __init__(self, account_name, api_key):
        self.client = LighterClient(api_key=api_key, sub_account_name=account_name)

    def place_market_order(self, symbol, side, size):
        return self.client.place_order(
            market=symbol,
            side=side,
            size=size,
            type="market"
        )

    def close_all_positions(self):
        positions = self.client.get_positions()
        for p in positions:
            if float(p['size']) != 0:
                side = 'sell' if p['side'] == 'buy' else 'buy'
                self.place_market_order(p['market'], side, abs(float(p['size'])))


# bot.py
import time
from lighter_client import LighterBot

# Load API keys and sub-account names
API_KEY_1 = os.getenv("API_KEY_1")
API_KEY_2 = os.getenv("API_KEY_2")
ACCOUNT_1 = os.getenv("ACCOUNT_1")
ACCOUNT_2 = os.getenv("ACCOUNT_2")

bot1 = LighterBot(ACCOUNT_1, API_KEY_1)
bot2 = LighterBot(ACCOUNT_2, API_KEY_2)

def run_trade_cycle(interval_minutes=2, symbol="ETH-PERP", size=0.01):
    print(f"Placing trades... (interval: {interval_minutes} minutes)")
    bot1.place_market_order(symbol, "buy", size)  # LONG
    bot2.place_market_order(symbol, "sell", size) # SHORT

    print(f"Sleeping for {interval_minutes} minutes...")
    time.sleep(interval_minutes * 60)

    print("Closing trades...")
    bot1.close_all_positions()
    bot2.close_all_positions()


# schedule.py
import argparse
from bot import run_trade_cycle

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=int, choices=[2, 5, 10], required=True, help="Trade cycle interval (minutes)")
    parser.add_argument("--symbol", default="ETH-PERP", help="Market symbol to trade")
    parser.add_argument("--size", type=float, default=0.01, help="Order size")
    args = parser.parse_args()

    run_trade_cycle(interval_minutes=args.interval, symbol=args.symbol, size=args.size)


# .env.example
API_KEY_1=your_testnet_api_key_for_account_1
API_KEY_2=your_testnet_api_key_for_account_2
ACCOUNT_1=your_sub_account_1_name
ACCOUNT_2=your_sub_account_2_name


# requirements.txt
lighter-sdk==0.1.3
python-dotenv


# README.md
# Lighter Dual-Side Trading Bot

This bot opens simultaneous LONG and SHORT trades using two sub-accounts on Lighter Testnet and closes them after a selected interval (2, 5, or 10 minutes).

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env`:
```
API_KEY_1=...
API_KEY_2=...
ACCOUNT_1=...
ACCOUNT_2=...
```

3. Run bot:
```bash
python schedule.py --interval 5 --symbol ETH-PERP --size 0.01
