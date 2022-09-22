# -*- coding: utf-8 -*-
import logging
from collections import defaultdict
from datetime import datetime
from functools import lru_cache
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)


class NetWorth:
    def __init__(self):
        self.asset_dict = defaultdict(lambda: [0, 0])
        self.historical_net_worths = Path("data", "net_worth_history", "net_worth_history.csv")
        print("Welcome to your Net Worth Software. All prices are in CAD.")

    def find_net_worth(self):
        """Main method for calling all subcategories of net worth"""
        tfsa = self._tfsa()
        td = self._rrsp_td()
        rrsp = self._rrsp_nb()
        bitbuy = self._crypto_bitbuy()
        vet = self._crypto_vechain()
        theta = self._crypto_theta()
        twt = self._crypto_trust_wallet_token()
        shakepay = self._crypto_shakepay()
        binance = self._crypto_binance()
        home = self._home_cash()
        coinbase = self._crypto_coinbase()
        coinbase_wallet = self._crypto_coinbase_wallet()
        ledger = self._crypto_ledger()
        money_dict = dict(
            binance=binance,
            home=home,
            coinbase_wallet=coinbase_wallet,
            coinbase=coinbase,
            ledger=ledger,
            shakepay=shakepay,
            twt=twt,
            theta=theta,
            vet=vet,
            bitbuy=bitbuy,
            rrsp=rrsp,
            td=td,
            tfsa=tfsa,
        )
        total = sum(money_dict.values())
        print(f"\n\nYour net worth is ${total:.2f}!")
        print("\n" * 10)
        for key, value in self.asset_dict.items():
            print(f"{key:<10} {value[0]:<10.3f} {value[1]:<10}")
        self._save_history(money_dict=money_dict)

    def _crypto_trust_wallet_token(self) -> float:
        return self._process_csv_live_values(csv_file=Path("data", "money", "crypto", "trust_wallet.csv"))

    def _crypto_ledger(self) -> float:
        return self._process_csv_live_values(csv_file=Path("data", "money", "crypto", "ledger.csv"))

    def _crypto_coinbase(self) -> float:
        return self._process_csv_live_values(csv_file=Path("data", "money", "crypto", "coinbase.csv"))

    def _home_cash(self) -> float:
        return self._process_csv_static_values(csv_file=Path("data", "money", "home", "cash.csv"))

    def _rrsp_nb(self) -> float:
        return self._process_csv_static_values(csv_file=Path("data", "money", "home", "rrsp_nb.csv"))

    def _rrsp_td(self) -> float:
        return self._process_csv_static_values(csv_file=Path("data", "money", "home", "rrsp_td.csv"))

    def _tfsa(self):
        return self._process_csv_live_values(csv_file=Path("data", "money", "home", "tfsa.csv"))

    def _crypto_coinbase_wallet(self):
        return self._process_csv_live_values(csv_file=Path("data", "money", "crypto", "coinbase_wallet.csv"))

    def _crypto_binance(self):
        return self._process_csv_live_values(csv_file=Path("data", "money", "crypto", "binance.csv"))

    def _crypto_shakepay(self):
        return self._process_csv_live_values(csv_file=Path("data", "money", "crypto", "shakepay.csv"))

    def _crypto_theta(self):
        return self._process_csv_live_values(csv_file=Path("data", "money", "crypto", "theta_wallet.csv"))

    def _crypto_vechain(self):
        return self._process_csv_live_values(csv_file=Path("data", "money", "crypto", "vechain.csv"))

    def _crypto_bitbuy(self):
        return self._process_csv_live_values(csv_file=Path("data", "money", "crypto", "bitbuy.csv"))

    def _process_csv_static_values(self, csv_file: Path) -> float:
        """Multiply amount of asset by value"""
        print("*************************************************************************************************")
        df = pd.read_csv(csv_file)
        running_sum = 0
        for col in range(df.shape[1]):
            column = df.columns.to_list()[col]
            amount = df.iloc[0][column]
            running_sum += amount
            print(f"{'Current':<10} {column:<10} {'holding=$':<9}{amount:<50}")
        running_sum = round(running_sum, 2)
        print(f"The total sum for {csv_file.stem} is ${running_sum}")
        print("*************************************************************************************************")
        return running_sum

    def _process_csv_live_values(self, csv_file: Path) -> float:
        """Multiply amount of asset by value"""
        print("*************************************************************************************************")
        df = pd.read_csv(csv_file)
        running_sum = 0
        for col in range(df.shape[1]):
            column = df.columns.to_list()[col]
            ticker = self._get_price_yfinance(column=column)
            price = ticker.info["regularMarketPrice"]
            if not price:
                logger.warning(f"Failed to find price for {column}.")
                price = 0
            amount = df.iloc[0][column]
            value = round(amount * price, 2)
            running_sum += value
            print(f"{'Current':<10} {column:<10} {'holding=$':<9}{value:<50} {amount:<20} {price:<20}")
            self.asset_dict[column][0] += amount
            self.asset_dict[column][1] += value
        running_sum = round(running_sum, 2)
        print(f"The total sum for {csv_file.stem} is ${running_sum}")
        print("*************************************************************************************************")
        return running_sum

    def _save_history(self, money_dict: dict) -> None:
        """Save price history to csv and show plat"""
        date = datetime.today().strftime("%Y-%m-%d")
        net_worth = sum(money_dict.values())
        data = [
            [
                date,
                net_worth,
                money_dict["binance"],
                money_dict["home"],
                money_dict["coinbase_wallet"],
                money_dict["coinbase"],
                money_dict["ledger"],
                money_dict["shakepay"],
                money_dict["twt"],
                money_dict["theta"],
            ]
        ]
        df = pd.read_csv(str(self.historical_net_worths), parse_dates=["date"])
        df_new = pd.DataFrame(
            data,
            columns=[
                "date",
                "net_worth",
                "binance",
                "home",
                "coinbase_wallet",
                "coinbase",
                "ledger",
                "shakepay",
                "twt",
                "theta",
            ],
        )
        if date == df.at[df.shape[0] - 1, "date"].strftime("%Y-%m-%d"):
            # drop last row if last row was today
            df = df[:-1]
        df = pd.concat([df, df_new])
        df = df.astype({"net_worth": "float", "binance": "float"})
        df.to_csv(str(self.historical_net_worths), index=False)
        logger.info("Saved net worth to history!")
        plt.plot(df.date, df.net_worth, "bx-", label="net worth")
        plt.plot(df.date, df.binance, "rx-", label="binance")
        plt.plot(df.date, df.home, "kx-", label="home")
        plt.plot(df.date, df.coinbase_wallet, "gx-", label="coinbase_wallet")
        plt.plot(df.date, df.coinbase, "yx-", label="coinbase")
        plt.plot(df.date, df.ledger, "rx-", label="ledger")
        plt.plot(df.date, df.shakepay, "mx-", label="shakepay")
        plt.plot(df.date, df.twt, "yx-", label="twt")
        plt.plot(df.date, df.theta, "rx-", label="theta")
        plt.axhline(y=100000, color="y", linestyle="-")
        plt.title("Net Worth over time for Sergei Issaev")
        plt.xlabel("Date")
        plt.ylabel("Net Worth")
        plt.legend()
        plt.show()

    @staticmethod
    @lru_cache(maxsize=128)
    def _get_price_yfinance(column: str):
        """Get price and cache the price"""
        return yf.Ticker(column)
