# -*- coding: utf-8 -*-
import logging

from finances.app.net_worth import NetWorth
from finances.app.net_worth_config import NET_WORTH_CONFIG


def main():
    my_worth = NetWorth.from_config(NET_WORTH_CONFIG)
    my_worth.find_net_worth()
    df = my_worth.save_history()
    my_worth.create_plots(df=df)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s:%(message)s")
    main()
