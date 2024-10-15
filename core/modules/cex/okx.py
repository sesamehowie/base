import ccxt
from typing import Self
import random
from web3 import Web3
from core.utils.networks import Network
from eth_account import Account
from eth_typing import HexStr
from core.utils.w3_manager import EthManager
from core.utils.helpers import sleeping
from core.utils.custom_wrappers import exception_handler_with_retry
from loguru import logger
from settings import (
    OKX_API_KEY,
    OKX_API_SECRET,
    OKX_PASSPHRASE,
    ACCEPTABLE_L1_GWEI,
    OKX_WITHDRAW_AMT,
)


class OKX:

    def __init__(
        self,
        account_name: str | int,
        private_key: str | HexStr,
        network: Network,
        user_agent: str,
        proxy: str,
    ) -> Self:

        self.api_key = OKX_API_KEY
        self.api_secret = OKX_API_SECRET
        self.passphrase = OKX_PASSPHRASE
        self.exchange = ccxt.okx(
            {
                "apiKey": self.api_key,
                "secret": self.api_secret,
                "password": self.passphrase,
                "enableRateLimit": True,
            }
        )
        self.logger = logger
        self.private_key = private_key
        self.account_name = account_name
        self.account = Account.from_key(self.private_key)
        self.address = self.address = Web3.to_checksum_address(self.account.address)
        self.network = network
        self.user_agent = user_agent
        self.proxy = proxy
        self.client = EthManager(
            account_name=self.account_name,
            private_key=self.private_key,
            network=self.network,
            user_agent=self.user_agent,
            proxy=self.proxy,
        )
        self.module_name = "OKX"

        self.logger.debug(f"Now working: module {self.module_name}")

    @exception_handler_with_retry
    def withdraw_native(self, chain=None):
        from config import (
            OKX_CHAIN_NATIVE_MAPPING,
            OKX_FEES,
            OKX_SIGNIFICANT_DECIMALS,
        )

        if chain is None:
            chain = self.client.network.name

        if self.client.network.name == "Ethereum Mainnet":
            while True:
                try:
                    gas_price = self.client.w3.eth.gas_price

                    if gas_price < Web3.to_wei(ACCEPTABLE_L1_GWEI, "gwei"):
                        break
                    sleeping(mode=1)
                except Exception:
                    sleeping(mode=1)

        token_chain = OKX_CHAIN_NATIVE_MAPPING[chain]

        symbol_withdraw, network = (
            token_chain[: token_chain.find("-")],
            token_chain[token_chain.find("-") + 1 :],
        )

        fee = OKX_FEES[chain]

        amounts = OKX_WITHDRAW_AMT[0], OKX_WITHDRAW_AMT[1]
        amount_to_withdraw = random.uniform(amounts[0], amounts[1])

        sigs = (
            OKX_SIGNIFICANT_DECIMALS[token_chain],
            OKX_SIGNIFICANT_DECIMALS[token_chain] + 2,
        )

        amount_to_withdraw = round(amount_to_withdraw, random.randint(sigs[0], sigs[1]))

        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Withdrawing {amount_to_withdraw} {symbol_withdraw} to {self.client.network.name}"
        )

        dest_init_balance = self.client.get_eth_balance()

        self.exchange.withdraw(
            symbol_withdraw,
            amount_to_withdraw,
            self.address,
            params={
                "toAddress": self.address,
                "chainName": token_chain,
                "dest": 4,
                "fee": fee,
                "pwd": "-",
                "amt": amount_to_withdraw,
                "network": network,
            },
        )

        sleeping(mode=1)

        return self.client.wait_for_funds_on_dest_chain(
            destination_network=self.network, original_balance=dest_init_balance
        )
