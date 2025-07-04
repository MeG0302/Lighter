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
