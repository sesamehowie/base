import json
from web3 import Web3
from typing import Self
from loguru import logger
from eth_typing import HexStr
from config import WORKING_DIR
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

        self.module_name = "Relay"

        self.logger.debug(f"Now working: module {self.module_name}")

    @staticmethod
    def get_maker_data(from_id: int, to_id: int, token_name: str):

        paths = [
            "orbiter_maker1.json",
            "orbiter_maker2.json",
            "orbiter_maker3.json",
            "orbiter_maker4.json",
            "orbiter_maker5.json",
        ]
        for path in paths:
            try:
                with open(WORKING_DIR + f"\\src\\data\\services\\{path}") as file:
                    data = json.load(file)

                maker_data = data[f"{from_id}-{to_id}"][f"{token_name}-{token_name}"]

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

    def bridge(self, chain_from_id: int, bridge_data: tuple, need_check: bool = False):
        (
            from_chain,
            to_chain,
            amount,
            to_chain_id,
            from_token_name,
            to_token_name,
            from_token_address,
            to_token_address,
        ) = bridge_data

        if not need_check:
            bridge_info = f'{amount} {from_token_name} from {from_chain["name"]} to {to_chain["name"]}'
            self.logger_msg(
                *self.client.acc_info, msg=f"Bridge on Orbiter: {bridge_info}"
            )

        bridge_data = self.get_maker_data(
            from_chain["id"], to_chain["id"], from_token_name
        )
        destination_code = 9000 + to_chain["id"]
        decimals = self.client.get_decimals(token_address=from_token_address)
        fee = int(float(bridge_data["fee"]) * 10**decimals)
        amount_in_wei = self.client.to_wei(amount, decimals)
        full_amount = int(round(amount_in_wei + fee, -4) + destination_code)

        if need_check:
            return round(float(fee / 10**decimals), 6)

        min_price, max_price = bridge_data["min_amount"], bridge_data["max_amount"]

        if from_token_name != self.client.network.token:
            contract = self.client.get_contract(from_token_address)

            transaction = contract.functions.transfer(
                Web3.to_checksum_address(bridge_data["maker"]), full_amount
            ).build_transaction(
                {
                    "from": self.address,
                    "nonce": self.client.w3.eth.get_transaction_count(self.address),
                    "chainId": self.network.chain_id,
                }
            )
        else:
            transaction = self.client.get_tx_params(
                value=full_amount,
                to_address=Web3.to_checksum_address(bridge_data["maker"]),
            )

        if min_price <= amount <= max_price:
            if int(f"{full_amount}"[-4:]) != destination_code:
                raise SoftwareException(
                    "Math problem in Python. Machine will save your money =)"
                )

            signed = self.client.sign_transaction(transaction)

            if signed:
                tx_hash = self.client.send_tx(signed_tx=signed)

                if tx_hash:

                    self.logger.success(
                        f"{self.account_name} | {self.address} | {self.module_name} | Bridge complete. Note: wait a little for receiving funds",
                    )

                    return self.client.wait_for_funds_on_dest_chain(
                    )

        else:
            raise BridgeException(
                f"Limit range for bridge: {min_price} – {max_price} {from_token_name}!"
            )
