'''
Asset class
'''
from ast import Dict
import json
import time
import traceback

import requests

from state_variables import *


class Asset:
    def __init__(self, asset, requestId):
        self.asset = (asset,)
        self.requestId = (requestId,)
        self.price = (0,)
        self.string_price = ("0",)
        self.timestamp = (0,)
        self.last_pushed_price = (0,)
        self.time_last_pushed = 0

        self.api_list = []
        self.precision = 1e6

    def add_api_endpoint(self, api):
        self.api_list.append(api)

    def update_price(self):
        self.timestamp = int(time.time())
        self.price = int(self.medianize())

    def medianize(self):
        """
        Medianizes price of an asset from a selection of centralized price APIs
        """
        final_results = []
        didGet = False
        n = 0
        if not self.api_list:
            raise ValueError(
                "Cannot medianize prices of empty list. No APIs added for asset."
            )

        for api in self.api_list:
            price = self.get_price(api)
            final_results.append(price * self.precision)
        didGet = True

        # sort final results
        final_results.sort()
        return final_results[len(final_results) // 2]

    def get_price(api_info: Dict) -> float:
        """
        Fetches price data from centralized public web API endpoints
        Returns: (str) ticker price from public exchange web APIs
        Input: (list of str) public api endpoint with any necessary json parsing keywords
        """
        try:
            # Request JSON from public api endpoint
            rsp = requests.get(api_info["url"]).json()

            # Parse through json with pre-written keywords
            for keyword in api_info["keywords"]:
                rsp = rsp[keyword]

            # return price (last remaining element of the json)
            price = float(rsp)
            return price

        except Exception as e:
            api_err_msg = f'API ERROR {api_info["url"]}\n'
            tb = str(traceback.format_exc())
            msg = api_err_msg + str(e) + "\n" + tb
            signer_log.error(msg)

    def __str__(self):
        return f"""Asset: {self.name} request_id: {self.request_id} price: {self.price} timestamp: {self.timestamp}"""

    def __repr__(self):
        return f"""Asset: {self.name} request_id: {self.request_id} price: {self.price} timestamp: {self.timestamp}"""

    def __eq__(self, other):
        if self.name == other.name and self.request_id == other.request_id:
            return True
        return False