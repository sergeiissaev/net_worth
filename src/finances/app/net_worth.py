# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
from collections import defaultdict
from datetime import datetime
from functools import lru_cache
from pathlib import Path

import matplotlib.dates as mdates
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
        print("Welcome to your Net Worth Software.")

    def find_net_worth(self):
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
        self._report_total_holdings()

    def _report_total_holdings(self) -> None:
        print("\n" * 3)
        print("Combined holdings for each asset (sorted)")
        print("________________________________________________________")
        print()
        for key, value in sorted(self.asset_dict.items(), key=lambda x: x[1][1]):
            print(f"{key:<10} {value[0]:<10.3f} units      ${value[1]:<10.2f}")
        total = sum(self.money_dict.values())
        print(f"\n\nYour net worth is ${total:.2f}!")

    def _process_csv_static_values(self, df: pd.DataFrame, file_name: str) -> float:
        """Multiply amount of asset by value"""
        print("*************************************************************************************************")
        running_sum = 0
        for col in range(1, df.shape[1]):
            column = df.columns.to_list()[col]
            amount = df.iloc[0][column]
            running_sum += amount
            print(f"{'Current':<10} {column:<10} {'holding=$':<9}{amount:<50}")
            self.asset_dict[column][0] += amount  # of asset
            self.asset_dict[column][1] += amount  # in fiat
        self._print_running_sum(file_name=file_name, running_sum=running_sum)
        return running_sum

    def _process_csv_live_values(self, df: pd.DataFrame, file_name: str) -> float:
        """Multiply amount of asset by value"""
        print("*************************************************************************************************")
        running_sum = 0
        for col in range(1, df.shape[1]):
            column = df.columns.to_list()[col]
            try:
                price = self._get_price_yfinance(column=column)
            except TimeoutError:
                price = self._get_price_yfinance(column=column)
            except IndexError:
                price = self._get_price_yfinance(column=column)
            except Exception as e:
                logger.warning(f"Failed to find price for {column}. {e}")
                price = 0
            amount = df.iloc[0][column]
            value = round(amount * price, 2)
            running_sum += value
            print(
                f"{'Current':<10} {column:<10} {'holding=$':<9}{value:<50} {amount:<8.2f} {'units':<10} {price:<10.2f} {'$/unit':<10}"
            )
            self.asset_dict[column][0] += amount  # of asset
            self.asset_dict[column][1] += value  # in fiat
        self._print_running_sum(file_name=file_name, running_sum=running_sum)
        return running_sum

    def _print_running_sum(self, file_name: str, running_sum: float) -> None:
        running_sum = round(running_sum, 2)
        self.money_dict[file_name] = running_sum
        print(f"The total sum for {file_name} is ${running_sum}")
        print("*************************************************************************************************")

    def save_history(self) -> pd.DataFrame:
        """Save price history to csv and show plat"""
        date = datetime.today().strftime("%Y-%m-%d")
        net_worth = sum(self.money_dict.values())
        self.money_dict["date"] = date
        self.money_dict["net_worth"] = net_worth
        df_new = pd.DataFrame.from_dict(self.money_dict, orient="index").T
        df_new.date = pd.to_datetime(df_new.date)
        # If an existing net worth file is not found
        if not self.historical_net_worths.is_file():
            # If the entire folder is missing
            if not self.historical_net_worths.parent.is_dir():
                self.historical_net_worths.parent.mkdir(parents=True)
            # Ensure first two columns are date and net_worth
            df_new.insert(0, "net_worth", df_new.pop("net_worth"))
            df_new.insert(0, "date", df_new.pop("date"))
            df = df_new
        else:
            df = pd.read_csv(str(self.historical_net_worths), parse_dates=["date"])
            if date == df.at[df.shape[0] - 1, "date"].strftime("%Y-%m-%d"):
                # drop last row if last row was today
                df = df[:-1]
            df = pd.concat([df, df_new])
        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        if df["net_worth"].max() == df["net_worth"].iloc[-1]:
            print("CONGRATS ON THE NEW ALL TIME HIGH!!!!")
            print(":D :D :D :D :D :D :D :D :D")
        df.to_csv(str(self.historical_net_worths), index=False)
        logger.info("Saved net worth to history!")
        return df

    def create_plots(self, df: pd.DataFrame) -> None:
        """Create plots of net worth"""
        self._create_line_plot(df=df)
        self._create_stacked_plot(df=df)

    def _create_line_plot(self, df: pd.DataFrame) -> None:
        """Create line plot of net worth"""
        for col in df.columns[1:]:  # skip date
            plt.plot(df.date, df[col], label=col)
        plt.title("Net Worth over time")
        plt.xlabel("Date")
        plt.xticks(rotation=30)
        plt.gca().xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[4, 7, 10]))
        plt.ylabel("Net Worth")
        plt.legend(prop={"size": 6})
        plt.tight_layout()
        plt.savefig(Path("data", "processed", "net_worth_line_graph.png"))
        plt.show()

    def _create_stacked_plot(self, df: pd.DataFrame) -> None:
        """Create stacked plot of net worth"""
        fig, ax = plt.subplots()
        ax.stackplot(df.date, df.iloc[:, 2:].T, labels=list(df.iloc[:, 2:].columns))  # skip date and net worth
        ax.plot(df.date, df.net_worth, label="net_worth")
        ax.legend(loc="lower left")
        ax.set_title("Net Worth Stacked Plot")
        ax.set_xlabel("Date")
        ax.set_ylabel("Net Worth")
        fig.autofmt_xdate()
        plt.tight_layout()
        plt.savefig(Path("data", "processed", "net_worth_stacked_graph.png"))
        plt.show()

    @staticmethod
    @lru_cache(maxsize=128)
    def _get_price_yfinance(column: str):
        """Get price and cache the price"""
        return yf.Ticker(column).fast_info["last_price"]
