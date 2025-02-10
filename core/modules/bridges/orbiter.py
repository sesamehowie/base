import os
import json
import random
from web3 import Web3
from typing import Self
from pathlib import Path
from loguru import logger
from eth_typing import HexStr
from config import WORKING_DIR
from settings import ORBITER_FROM_TOKEN, ORBITER_TO_TOKEN, ORBITER_AMT_RANGE
from eth_account import Account
from core.utils.networks import Network
from core.clients.evm_client import EvmClient
from core.utils.decorators import retry_execution
from core.utils.exceptions import SoftwareException, BridgeException


class Orbiter:
    def __init__(
        self,
        account_name: str | int,
        private_key: str | HexStr,
        network: Network,
        user_agent: str,
        proxy: str,
    ) -> Self:

        self.logger = logger
        self.private_key = private_key
        self.account_name = account_name
        self.account = Account.from_key(self.private_key)
        self.address = self.address = Web3.to_checksum_address(self.account.address)
        self.network: Network = network
        self.user_agent = user_agent
        self.proxy = proxy

        self.client = EvmClient(
            account_name=self.account_name,
            private_key=self.private_key,
            network=self.network,
            user_agent=self.user_agent,
            proxy=self.proxy,
        )

        self.module_name = "Orbiter Finance"

        self.logger.debug(f"Now working: module {self.module_name}")

        self.internal_ids = {
            "Ethereum": 1,
            "Arbitrum": 2,
            "Polygon": 6,
            "Optimism": 7,
            "Scroll": 19,
            "Base": 21,
            "Linea": 23,
            "Zora": 30,
        }

    def get_maker_data(self, to_chain: Network):

        paths = [
            "orbiter_maker1.json",
            "orbiter_maker2.json",
            "orbiter_maker3.json",
            "orbiter_maker4.json",
            "orbiter_maker5.json",
            "orbiter_maker6.json",
            "orbiter_maker7.json",
        ]
        for path in paths:
            try:
                data = json.load(
                    open(os.path.join(WORKING_DIR, Path(f"data/makers/{path}")))
                )

                maker_data = data[
                    f"{self.internal_ids[self.network.name]}-{self.internal_ids[to_chain.name]}"
                ][f"{ORBITER_FROM_TOKEN}-{ORBITER_TO_TOKEN}"]

                bridge_data = {
                    "maker": maker_data["makerAddress"],
                    "fee": maker_data["tradingFee"],
                    "min_amount": maker_data["minPrice"],
                    "max_amount": maker_data["maxPrice"],
                }

                if bridge_data:
                    return bridge_data
            except KeyError:
                pass

        raise BridgeException("That bridge is not active!")

    @retry_execution
    def bridge(
        self,
        to_chain: Network,
        need_check: bool = False,
        percentages: tuple[str, str] | None = None,
        amount_range: list[float | float] = ORBITER_AMT_RANGE,
    ):
        from_chain = self.network
        from_token_name = ORBITER_FROM_TOKEN

        if percentages:
            amount = self.client.get_human_amount(
                self.client.get_percentile(percentages=percentages)
                - Web3.to_wei(0.0002, "ether")
            )
        elif amount_range:
            amount = round(random.uniform(amount_range[0], amount_range[1]), 6)

        if not need_check:
            bridge_info = (
                f"{amount} {from_token_name} from {from_chain.name} to {to_chain.name}"
            )
            self.logger.info(
                f"{self.account_name} | {self.address} | {self.module_name} | Bridge: {bridge_info}"
            )

        bridge_data = self.get_maker_data(to_chain=to_chain)
        destination_code = 9000 + self.internal_ids[to_chain.name]
        decimals = 18 if from_token_name == "ETH" else 6
        fee = int(float(bridge_data["fee"]) * 10**decimals)
        amount_in_wei = self.client.to_wei(amount, decimals)
        full_amount = int(round(amount_in_wei + fee, -4) + destination_code)

        if need_check:
            return round(float(fee / 10**decimals), 6)

        min_price, max_price = bridge_data["min_amount"], bridge_data["max_amount"]
        transaction = self.client.get_tx_params(
            value=full_amount,
            to_address=Web3.to_checksum_address(bridge_data["maker"]),
        )
        if min_price <= amount <= max_price:
            if int(f"{full_amount}"[-4:]) != destination_code:
                raise SoftwareException(
                    "Math problem in Python. Machine will save your money =)"
                )
            dest_client = EvmClient(
                account_name=self.account_name,
                private_key=self.private_key,
                network=to_chain,
                user_agent=self.user_agent,
                proxy=self.proxy,
            )
            init_balance = dest_client.get_eth_balance()
            signed = self.client.sign_transaction(transaction)
            if signed:
                tx_hash = self.client.send_tx(signed_tx=signed)
                if tx_hash:
                    self.logger.success(
                        f"{self.account_name} | {self.address} | {self.module_name} | Bridge complete. Note: wait a little for receiving funds",
                    )
                    return self.client.wait_for_funds_on_dest_chain(
                        destination_network=to_chain, original_balance=init_balance
                    )
        else:
            raise BridgeException(
                f"Limit range for bridge: {min_price} – {max_price} {from_token_name}!"
            )
