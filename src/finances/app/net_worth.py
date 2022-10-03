# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
from collections import defaultdict
from datetime import datetime
from functools import lru_cache
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

from finances.template import _Template

logger = logging.getLogger(__name__)


class NetWorth(_Template):
    data_files_path: Path
    historical_net_worths: Path

    def __init__(self, data_files_path: Path, historical_net_worths: Path):
        self.historical_net_worths = historical_net_worths
        self.data_files_path = data_files_path
        self.asset_dict = defaultdict(lambda: [0, 0])
        self.money_dict = {}
        print("Welcome to your Net Worth Software. All prices are in CAD.")
        self._find_net_worth()

    def _find_net_worth(self):
        """Main method for calling all subcategories of net worth"""
        for data_file in self.data_files_path.glob("**/*.csv"):
            df = pd.read_csv(data_file)
            file_type = int(df.type)
            file_name = data_file.stem
            if file_type == 1:
                self._process_csv_live_values(df=df, file_name=file_name)
            elif file_type == 2:
                self._process_csv_static_values(df=df, file_name=file_name)
            else:
                err = ValueError(f"Invalid file type: {file_type=}")
                logger.error(err)
                raise err
        total = sum(self.money_dict.values())
        print(f"\n\nYour net worth is ${total:.2f}!")
        print("\n" * 10)
        for key, value in self.asset_dict.items():
            print(f"{key:<10} {value[0]:<10.3f} {value[1]:<10}")
        self._save_history(money_dict=self.money_dict)

    def _process_csv_static_values(self, df: pd.DataFrame, file_name: str) -> float:
        """Multiply amount of asset by value"""
        print("*************************************************************************************************")
        running_sum = 0
        for col in range(1, df.shape[1]):
            column = df.columns.to_list()[col]
            amount = df.iloc[0][column]
            running_sum += amount
            print(f"{'Current':<10} {column:<10} {'holding=$':<9}{amount:<50}")
            self.asset_dict[column][0] += amount
        running_sum = round(running_sum, 2)
        self.money_dict[file_name] = running_sum
        print(f"The total sum for {file_name} is ${running_sum}")
        print("*************************************************************************************************")
        return running_sum

    def _process_csv_live_values(self, df: pd.DataFrame, file_name: str) -> float:
        """Multiply amount of asset by value"""
        print("*************************************************************************************************")
        running_sum = 0
        for col in range(1, df.shape[1]):
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
        self.money_dict[file_name] = running_sum
        print(f"The total sum for {file_name} is ${running_sum}")
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
                money_dict["vet"],
                money_dict["bitbuy"],
                money_dict["rrsp"],
                money_dict["td"],
                money_dict["tfsa"],
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
                "vet",
                "bitbuy",
                "rrsp",
                "td",
                "tfsa",
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
        plt.plot(df.date, df.vet, "yx-", label="vet")
        plt.plot(df.date, df.bitbuy, "gx-", label="bitbuy")
        plt.plot(df.date, df.rrsp, "yx-", label="rrsp")
        plt.plot(df.date, df.td, "yx-", label="td")
        plt.plot(df.date, df.tfsa, "rx-", label="tfsa")
        plt.axhline(y=100000, color="y", linestyle="-")
        plt.title("Net Worth over time for Sergei Issaev")
        plt.xlabel("Date")
        plt.ylabel("Net Worth")
        plt.legend(prop={"size": 6})
        plt.show()
        fig, ax = plt.subplots()
        ax.stackplot(df.date, df.iloc[:, 2:].T, labels=list(df.iloc[:, 2:].columns))
        ax.plot(df.date, df.net_worth, label="net_worth")
        ax.legend(loc="lower left")
        plt.show()

    @staticmethod
    @lru_cache(maxsize=128)
    def _get_price_yfinance(column: str):
        """Get price and cache the price"""
        return yf.Ticker(column)
