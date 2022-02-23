import argparse
import csv
import logging
import os
import random
import sys
import time
import traceback
from typing import Dict
from typing import List

import requests
import telebot
import yaml
from box import Box
from dotenv import find_dotenv
from dotenv import load_dotenv
from hexbytes import HexBytes
from web3 import Web3
from web3.middleware import geth_poa_middleware

from pysigner.asset import Asset
from pysigner.config import get_configs


class TellorSigner:
    def __init__(self, cfg, private_key, asset):
        self.cfg = cfg

        load_dotenv(find_dotenv())
        self.secret_test = os.getenv("TEST_VAR")

        with open("TellorMesosphere.json") as f:
            abi = f.read()

        network = self.cfg.network
        feeds = self.cfg.feeds

        # Only submit assets tipped on this network
        self.assets = [
            Asset(a, feeds[a].requestId)
            for a in feeds.keys()
            if feeds[a].networks != "none" and network in feeds[a].networks
        ]

        node = self.cfg.networks[network].node
        if network == "polygon":
            node += os.getenv("POKT_POLYGON")
        if network == "rinkeby":
            node += os.getenv("POKT_RINKEBY")
        self.explorer = self.cfg.networks[network].explorer
        self.chain_id = self.cfg.networks[network].chain_id

        self.w3 = Web3(Web3.HTTPProvider(node))

        # choose network from CLI flag
        if network == "rinkeby" or network == "mumbai" or network == "rinkeby-arbitrum":
            self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.mesosphere = self.w3.eth.contract(
            Web3.toChecksumAddress(self.cfg.address[network]), abi=abi
        )
        self.acc = self.w3.eth.default_account = self.w3.eth.account.from_key(
            private_key if private_key else os.getenv("PRIVATE_KEYS")
        )

        self.bot = None
        if os.getenv("TG_TOKEN") != None and os.getenv("CHAT_ID") != None:
            self.bot = telebot.TeleBot(os.getenv("TG_TOKEN"), parse_mode=None)


    def run(self):
        starting_balance = self.w3.eth.get_balance(self.acc.address)

        prev_alert = ""
        self.update_assets()

        nonce = self.w3.eth.get_transaction_count(self.acc.address)

        print("nonce:", nonce)

        # if signer balance is less than half an ether, send alert
        if self.w3.eth.get_balance(self.acc.address) < 5e14:
            msg = f"warning: signer balance now below .5 ETH\nCheck {self.explorer}/address/{self.acc.address}"
            prev_alert = self.bot_alert(msg, prev_alert, self.asset)

        tx = self.build_tx(
            self.asset,
            nonce,
            new_gas_price=self.cfg.gasprice,
            extra_gas_price=extra_gp,
        )

        tx_signed = (
            self.w3.eth.default_account.sign_transaction(tx)
        )

        tx_hash = self.w3.eth.send_raw_transaction(
            tx_signed.rawTransaction
        )

        print("waiting for tx receipt")
        _ = self.w3.eth.wait_for_transaction_receipt(
            tx_hash, timeout=self.cfg.receipt_timeout
        )
        print("received, tx sent")

        self.log_tx(self.asset, tx_hash)
        nonce += 1
        
        print(self.asset)

        self.asset.last_pushed_price = self.asset.price
        self.asset.time_last_pushed = self.asset.timestamp

        time.sleep(3600)
        print("sleeping...")
        # wait because contract only writes new values every 60 seconds

        curr_balance = self.w3.eth.get_balance(self.acc.address)
        if curr_balance < 0.005 * 1e18:
            time.sleep(60 * 15)


if __name__ == "__main__":
    cfg = get_configs(sys.argv[1:])
    signer = TellorSigner(cfg)
    signer.run()
