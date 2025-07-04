# lighter_client.py
import os
from lighter import LighterClient
from dotenv import load_dotenv

load_dotenv()

class LighterBot:
    def __init__(self, private_key: str):
        self.client = LighterClient(private_key=private_key)

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
