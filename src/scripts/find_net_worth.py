# -*- coding: utf-8 -*-
import logging

from finances.app.net_worth import NetWorth


def main():
    net = NetWorth()
    net.find_net_worth()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s:%(message)s")
    main()
