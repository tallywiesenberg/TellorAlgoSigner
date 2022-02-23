'''
Reporter class
'''

from pysigner.asset import Asset


class Reporter:
    def __init__(self, account, tg_bot):
        self.account = account

    def stake():
        pass

    def report():
        pass

    def build_tx(
        self,
        an_asset: Asset,
        new_nonce: int,
        new_gas_price: str,
        extra_gas_price: float,
    ) -> Dict:
        new_gas_price = str(float(new_gas_price) + extra_gas_price)

        transaction = self.mesosphere.functions.submitValue(
            an_asset.request_id, an_asset.price
        ).buildTransaction(
            {
                "nonce": new_nonce,
                "gas": 4000000,
                "gasPrice": self.w3.toWei(new_gas_price, "gwei"),
                "chainId": self.chain_id,
            }
        )

        return transaction

    def submit_value(self, asset):
        alert_sent = False
        try:
            assets = asset.update_price()
        except:
            if not alert_sent:
                tb = traceback.format_exec()
                self.tg_bot.send_message(tb)
                alert_sent = True
        for asset in assets:
            try:
                nonce = w3.eth.get_transaction_count(acc.address)
                print(nonce)
                # if signer balance is less than half an ether, send alert
                if (w3.eth.get_balance(acc.address) < 5e14) and ~alert_sent:
                    bot.send_message(
                        os.getenv("CHAT_ID"),
                        f"""warning: signer balance now below .5 ETH
          \nCheck {explorer}/address/"""
                        + acc.address,
                    )
                    alert_sent = True
                else:
                    alert_sent = False
                if (asset["timestamp"] - asset["timeLastPushed"] > 5) or (
                    abs(asset["price"] - asset["lastPushedPrice"]) > 0.05
                ):
                    tx = mesosphere.functions.submitValue(
                        asset["requestId"], asset["price"]
                    ).buildTransaction(
                        {
                            "nonce": nonce,
                            "gas": 4000000,
                            "gasPrice": w3.toWei("3", "gwei"),
                            "chainId": chainId,
                        }
                    )
                    tx_signed = w3.eth.default_account.sign_transaction(tx)
            except:
                if not alert_sent:
                    traceback = traceback.format_exec()
                    bot.send_message(traceback)
                    alert_sent = True
                try:
                    w3.eth.send_raw_transaction(tx_signed.rawTransaction)
                    print(asset["asset"])
                    print(asset["price"])

                    asset["lastPushedPrice"] = asset["price"]
                    asset["timeLastPushed"] = asset["timestamp"]
                    # nonce += 1
                    print("waiting to submit....")
                    time.sleep(5)
                except:
                    nonce += 1
                    if w3.eth.get_balance(acc.address) < 0.005 * 1e18:
                        bot.send_message(
                            os.getenv("CHAT_ID"),
                            f"""urgent: signer ran out out of ETH"
            \nCheck {explorer}/address/{acc.address}""",
                        )
                        time.sleep(60 * 15)
