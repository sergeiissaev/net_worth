import pandas as pd
from pathlib import Path
import yfinance as yf
import logging
from functools import lru_cache
logger = logging.getLogger(__name__)


class NetWorth:
    def __init__(self):
        print("Welcome to your Net Worth Software. All prices are in CAD.")

    def find_net_worth(self):
        '''Main method for calling all subcategories of net worth'''
        binance = self._crypto_binance()
        home = self._home_cash()
        coinbase = self._crypto_coinbase()
        coinbase_wallet = self._crypto_coinbase_wallet()
        ledger = self._crypto_ledger()
        total = sum([binance, home, coinbase_wallet, coinbase, ledger])
        print(f"\n\nYour net worth is ${total:.2f}!")

    def _crypto_ledger(self) -> float:
        return self._process_csv_live_values(csv_file=Path("data", "money", "crypto", "ledger.csv"))

    def _crypto_coinbase(self) -> float:
        return self._process_csv_live_values(csv_file=Path("data", "money", "crypto", "coinbase.csv"))

    def _home_cash(self) -> float:
        return self._process_csv_static_values(csv_file=Path("data", "money", "home", "cash.csv"))

    def _crypto_coinbase_wallet(self):
        return self._process_csv_live_values(csv_file=Path("data", "money", "crypto", "coinbase_wallet.csv"))

    def _crypto_binance(self):
        return self._process_csv_live_values(csv_file=Path("data", "money", "crypto", "binance.csv"))

    def _crypto_shakepay(self):
        self._process_csv_live_values(csv_file=Path("data", "crypto", "ledger.csv"))

    def _process_csv_static_values(self, csv_file: Path) -> float:
        '''Multiply amount of asset by value'''
        print("*************************************************************************************************")
        df = pd.read_csv(csv_file)
        running_sum = 0
        for col in range(df.shape[1]):
            column = df.columns.to_list()[col]
            amount = df.iloc[0][column]
            running_sum+= amount
            print(f"{'Current':<10} {column:<10} {'holding=$':<9}{amount:<50}")
        running_sum = round(running_sum, 2)
        print(f"The total sum for {csv_file.stem} is ${running_sum}")
        print("*************************************************************************************************")
        return running_sum

    def _process_csv_live_values(self, csv_file: Path) -> float:
        '''Multiply amount of asset by value'''
        print("*************************************************************************************************")
        df = pd.read_csv(csv_file)
        running_sum = 0
        for col in range(df.shape[1]):
            column = df.columns.to_list()[col]
            ticker = self._get_price_yfinance(column=column)
            price = ticker.info['regularMarketPrice']
            if not price:
                logger.warning(f"Failed to find price for {column}.")
                price = 0
            amount = df.iloc[0][column]
            value = round(amount * price, 2)
            running_sum+= value
            print(f"{'Current':<10} {column:<10} {'holding=$':<9}{value:<50} {amount:<20} {price:<20}")
        running_sum = round(running_sum, 2)
        print(f"The total sum for {csv_file.stem} is ${running_sum}")
        print("*************************************************************************************************")
        return running_sum

    @staticmethod
    @lru_cache(maxsize=128)
    def _get_price_yfinance(column: str):
        '''Get price and cache the price'''
        return yf.Ticker(column)
