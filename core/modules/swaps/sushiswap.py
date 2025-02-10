import time
import random
from typing import Self
from eth_typing import HexStr
from hexbytes import HexBytes
from core.clients.evm_client import EvmClient
from eth_account import Account
from web3 import Web3
from core.utils.networks import Network
from loguru import logger
from settings import SWAP_SLIPPAGE
from core.utils.decorators import retry_execution
from config import (
    SUSHISWAP_QUOTER,
    SUSHISWAP_ROUTER,
    SUSHISWAP_CONTRACTS,
    TOKENS_PER_CHAIN,
    ZERO_ADDRESS,
)


class SushiSwap:
    def __init__(
        self,
        account_name: str | int,
        private_key: str | HexStr,
        network: Network,
        user_agent: str,
        proxy: str,
    ) -> Self:
        self.private_key = private_key
        self.logger = logger
        self.account_name = account_name
        self.account = Account.from_key(self.private_key)
        self.address = self.address = Web3.to_checksum_address(self.account.address)
        self.network = network
        self.user_agent = user_agent
        self.proxy = proxy
        self.client = EvmClient(
            account_name=self.account_name,
            private_key=self.private_key,
            network=self.network,
            user_agent=self.user_agent,
            proxy=self.proxy,
        )
        self.module_name = "Sushiswap"
        self.default_headers = {"User-Agent": self.user_agent}
        self.default_proxies = {
            "http": f"http://{self.proxy}",
            "https": f"http://{self.proxy}",
        }

        self.logger.debug(f"Now working: module {self.module_name}")

        self.router_contract = self.client.get_contract(
            SUSHISWAP_CONTRACTS[self.network.name]["router"],
            SUSHISWAP_ROUTER,
        )
        self.quoter_contract = self.client.get_contract(
            SUSHISWAP_CONTRACTS[self.network.name]["quoter"],
            SUSHISWAP_QUOTER,
        )

    def get_path(
        self,
        from_token_address: str,
        to_token_address: str,
        from_token_name: str,
        to_token_name: str,
    ):

        pool_fee_info = {
            "Base": {
                "USDC.e/ETH": 500,
                "ETH/USDC.e": 500,
            },
            "Scroll": {
                "USDC/ETH": 3000,
                "ETH/USDC": 3000,
                "USDC/USDT": 1000,
                "USDT/USDC": 1000,
            },
        }[self.client.network.name]

        if "USDT" not in [from_token_name, to_token_name]:
            from_token_bytes = HexBytes(from_token_address).rjust(20, b"\0")
            to_token_bytes = HexBytes(to_token_address).rjust(20, b"\0")
            fee_bytes = pool_fee_info[f"{from_token_name}/{to_token_name}"].to_bytes(
                3, "big"
            )
            return from_token_bytes + fee_bytes + to_token_bytes
        else:
            from_token_bytes = HexBytes(from_token_address).rjust(20, b"\0")
            index_1 = f"{from_token_name}/USDC"
            fee_bytes_1 = pool_fee_info[index_1].to_bytes(3, "big")
            middle_token_bytes = HexBytes(
                TOKENS_PER_CHAIN[self.network.name]["USDC"]
            ).rjust(20, b"\0")
            index_2 = f"USDC/{to_token_name}"
            fee_bytes_2 = pool_fee_info[index_2].to_bytes(3, "big")
            to_token_bytes = HexBytes(to_token_address).rjust(20, b"\0")
            return (
                from_token_bytes
                + fee_bytes_1
                + middle_token_bytes
                + fee_bytes_2
                + to_token_bytes
            )

    def get_min_amount_out(self, path: bytes, amount_in_wei: int):
        min_amount_out, _, _, _ = self.quoter_contract.functions.quoteExactInput(
            path, amount_in_wei
        ).call()

        return int(min_amount_out - (min_amount_out / 100 * SWAP_SLIPPAGE * 2))

    @retry_execution
    def swap(
        self,
        from_token_name: str,
        to_token_name: str,
        amount_range: list[float, float],
        help_deposit: bool = False,
    ):
        amount = round(random.uniform(amount_range[0], amount_range[1]), 6)

        amount_in_wei = self.client.to_wei(amount=amount, decimals=18)

        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Swap: {amount} {from_token_name} -> {to_token_name}",
        )

        from_token_address = TOKENS_PER_CHAIN[self.network.name][from_token_name]
        to_token_address = TOKENS_PER_CHAIN[self.network.name][to_token_name]

        deadline = int(time.time()) + 1800
        path = self.get_path(
            from_token_address, to_token_address, from_token_name, to_token_name
        )
        min_amount_out = self.get_min_amount_out(path, amount_in_wei)

        if from_token_name != "ETH":
            self.client.check_allowance(
                from_token_address,
                SUSHISWAP_CONTRACTS[self.network.name]["router"],
                amount_in_wei,
            )

        tx_data = self.router_contract.encodeABI(
            fn_name="exactInput",
            args=[
                (
                    path,
                    self.client.address if to_token_name != "ETH" else ZERO_ADDRESS,
                    deadline,
                    amount_in_wei,
                    min_amount_out,
                )
            ],
        )

        full_data = [tx_data]

        if from_token_name == "ETH" or to_token_name == "ETH":
            tx_additional_data = self.router_contract.encodeABI(
                fn_name="unwrapWETH9" if from_token_name != "ETH" else "refundETH",
                args=(
                    [min_amount_out, self.client.address]
                    if from_token_name != "ETH"
                    else None
                ),
            )
            full_data.append(tx_additional_data)

        tx_params = self.client.get_tx_params(is_for_contract_tx=True)
        tx_params["value"] = amount_in_wei if from_token_name == "ETH" else 0
        transaction = self.router_contract.functions.multicall(
            full_data
        ).build_transaction(tx_params)

        signed = self.client.sign_transaction(tx_dict=transaction)

        if signed:
            return self.client.send_tx(signed_tx=signed)
