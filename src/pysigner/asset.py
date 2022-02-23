'''
Asset class
'''
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
            price = self.fetch_api(api)
            final_results.append(price * self.precision)
        didGet = True

        # sort final results
        final_results.sort()
        return final_results[len(final_results) // 2]

    def fetch_api(self, api):
        """
        Fetches price data from centralized public web API endpoints
        Returns: (str) ticker price from public exchange web APIs
        Input: (list of str) public api endpoint with any necessary json parsing keywords
        """
        if not self.api_list:
            raise ValueError("No APIs added for asset.")
        try:
            # Parse list input
            endpoint = api.url
            parsers = api.request_parsers

            # Request JSON from public api endpoint
            r = requests.get(endpoint)
            json_ = r.json()

            # Parse through json with pre-written keywords
            for keyword in parsers:
                json_ = json_[keyword]

            # return price (last remaining element of the json)
            price = json_
            return float(price)
        except:
            response = r.status_code
            print("API ERROR", api.url, " ", response)