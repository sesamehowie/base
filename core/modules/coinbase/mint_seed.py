from typing import Self
from eth_account import Account
from core.utils.w3_manager import EthManager
from web3 import Web3
import random
import time
from core.utils.helpers import sleeping
from eth_typing import HexStr
from loguru import logger
from core.utils.networks import Network
from core.utils.custom_wrappers import exception_handler_with_retry
from core.modules.coinbase.coinbase_wallet_mints import Mints


class SeedNft:
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
        self.account: Account = Account.from_key(self.private_key)
        self.address = self.address = Web3.to_checksum_address(self.account.address)
        self.network: Network = network
        self.user_agent = user_agent
        self.proxy = proxy
        self.client = EthManager(
            account_name=self.account_name,
            private_key=self.private_key,
            network=self.network,
            user_agent=self.user_agent,
            proxy=self.proxy,
        )
        self.module_name = "Pixotchi Seed NFT"

        self.logger.debug(f"Now working: module {self.module_name}")

    def get_seed_token_balance(self) -> int | float:
        from config import SEED_TOKEN_ADDR, SEED_TOKEN_ABI

        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Checking $SEED token balance..."
        )

        contract = self.client.get_contract(
            contract_addr=SEED_TOKEN_ADDR, abi=SEED_TOKEN_ABI
        )

        balance_wei = contract.functions.balanceOf(self.address).call()

        if balance_wei != 0:
            balance = round(balance_wei / 10**18, 4)
            self.logger.info(
                f"{self.account_name} | {self.address} | {self.module_name} | Your $SEED balance is {balance}"
            )
            return balance

        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Your $SEED balance is 0"
        )
        return 0

    def approve(self):
        from config import (
            SEED_MINTER_ADDR,
            SEED_TOKEN_ABI,
            SEED_TOKEN_ADDR,
            SEED_INF_APPROVE_AMT,
        )

        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Trying to infinite approve for Seed token..."
        )
        contract = self.client.get_contract(
            contract_addr=SEED_TOKEN_ADDR, abi=SEED_TOKEN_ABI
        )
        data = contract.encodeABI(
            fn_name="approve", args=[SEED_MINTER_ADDR, SEED_INF_APPROVE_AMT]
        )
        tx_params = self.client.get_tx_params(
            to_address=SEED_TOKEN_ADDR, value=0, data=data, default_gas=100000
        )

        signed = self.client.sign_transaction(tx_dict=tx_params)

        if signed:

            res = self.client.send_tx(signed_tx=signed)
            return res

        return

    def swap(self):
        from config import (
            SEED_SWAPPER_ADDR,
            SEED_ROUTER_ABI,
            SEED_TOKEN_ADDR,
            BASE_ETH_MASK,
        )

        balance = self.get_seed_token_balance()

        if balance < 5:
            approve_res = self.approve()

            if not approve_res:
                return False

        rand_flt = random.uniform(0.00006, 0.000065)
        random_amt = Web3.to_wei(rand_flt, "ether")

        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Trying to swap {rand_flt:.6f} ETH for SEED"
        )

        contract = self.client.get_contract(
            contract_addr=SEED_SWAPPER_ADDR, abi=SEED_ROUTER_ABI
        )

        timestamp = int(time.time())
        deadline = timestamp + 15 * 1000

        data = contract.encodeABI(
            fn_name="swapExactETHForTokens",
            args=[0, [BASE_ETH_MASK, SEED_TOKEN_ADDR], self.address, deadline],
        )

        tx_params = self.client.get_tx_params(
            to_address=SEED_SWAPPER_ADDR,
            value=random_amt,
            data=data,
            default_gas=150000,
        )

        signed = self.client.sign_transaction(tx_dict=tx_params)

        if signed:

            res = self.client.send_tx(signed_tx=signed)
            return res

        return

    @exception_handler_with_retry
    def mint(self):
        from config import SEED_MINTER_ADDR, SEED_MINTER_ABI

        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Minting..."
        )

        balance = self.get_seed_token_balance()

        if balance < 5:
            self.swap()
            sleeping(1)

        contract = self.client.get_contract(
            contract_addr=SEED_MINTER_ADDR, abi=SEED_MINTER_ABI
        )

        data = contract.encodeABI(
            fn_name="mint",
            args=[1],
        )

        tx_params = self.client.get_tx_params(
            to_address=SEED_MINTER_ADDR,
            value=0,
            data=data,
            default_gas=Mints.PixotchiSeed.default_gas,
        )

        signed = self.client.sign_transaction(tx_dict=tx_params)

        if signed:

            res = self.client.send_tx(signed_tx=signed)
            return res

        return
