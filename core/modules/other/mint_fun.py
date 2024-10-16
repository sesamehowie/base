import copy
import random
import time
from typing import Self
from eth_account import Account
from core.clients.evm_client import EvmClient
from web3 import Web3
import requests
from eth_typing import HexStr
from core.utils.helpers import sleeping
from loguru import logger
from core.utils.networks import Network
from core.utils.decorators import retry_execution
from config import MINTFUN_CONTRACTS, MINTFUN_ABI


class MintFun:
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
        self.module_name = "MintFun"

        self.logger.debug(f"Now working: module {self.module_name}")

    def wait_for_mint_same_chain(self, original_balance: int):
        from config import MAX_DST_WAIT_TIME, MAX_RETRIES

        exc_count = 0
        runtime = 0

        while True:
            if runtime > MAX_DST_WAIT_TIME:
                return False

            start = time.time()
            try:

                dst_bal = self.client.get_eth_balance()
                if dst_bal < original_balance:
                    self.logger.success(
                        f"{self.account_name} | {self.address} | {self.module_name} | Mint successful!"
                    )
                    sleeping(mode=1)
                    return True

                sleeping(mode=1)
                end = time.time()
                runtime += int(end - start)

            except Exception as e:
                self.logger.warning(
                    f"{self.account_name} | {self.address} | {self.module_name} | Something went wrong while waiting on balance change - {e}"
                )
                self.logger.warning(
                    f"{self.account_name} | {self.address} | {self.module_name} | Retrying..."
                )
                exc_count += 1

                if exc_count >= MAX_RETRIES:
                    self.change_rpc()

                sleeping(mode=3)
                end = time.time()

    def get_tx_data(self, contract_address):
        url = f"https://mint.fun/api/mintfun/contract/{self.client.network.chain_id}:{contract_address}/transactions"

        params = {"address": self.client.address}

        r = requests.get(
            url=url,
            params=params,
            headers={"User-Agent": self.user_agent},
            proxies={"http": f"http://{self.proxy}", "https": f"http://{self.proxy}"},
        )

        response = r.json()

        total_time = 0
        timeout = 10
        while True:
            for tx in response["transactions"]:
                if (
                    int(tx["nftCount"]) == 1
                    and tx["to"].lower() == contract_address.lower()
                    and tx["isValid"]
                ):
                    calldata = tx["callData"].replace(
                        "ec45d2d56ec37ffabeb503a27ae21ba806ebe075",
                        self.client.address[2:],
                    )
                    eth_value = int(tx["ethValue"])

                    return calldata, eth_value

            total_time += 10
            time.sleep(random.randint(8, 13))

            if total_time > timeout:
                raise Exception("Mint.fun doesnt have data for this mint!")

    @retry_execution
    def mint(self):
        mint_contracts = copy.deepcopy(MINTFUN_CONTRACTS)
        random.shuffle(mint_contracts)
        nft_contract = random.choice(mint_contracts)
        for i in (1, 2, 4):
            try:
                nft_contract = self.client.w3.to_checksum_address(nft_contract)

                calldata, eth_value = self.get_tx_data(nft_contract)

                contract = self.client.get_contract(
                    self.client.w3.to_checksum_address(nft_contract), MINTFUN_ABI[i]
                )

                try:
                    nft_name = contract.functions.name().call()
                except Exception:
                    nft_name = "Random"

                self.logger.info(
                    f"Mint {nft_name} NFT. Price: {eth_value / 10 ** 18:.6f} ETH",
                )

                transaction = self.client.get_tx_params(
                    value=eth_value,
                    to_address=nft_contract,
                    data=f"0x{calldata}",
                    default_gas=200000,
                )

                signed = self.client.sign_transaction(tx_dict=transaction)
                if signed:
                    init_balance = self.client.get_eth_balance()
                    self.client.send_tx(signed_tx=signed)
                    return self.wait_for_mint_same_chain(original_balance=init_balance)

            except Exception as error:
                self.logger.error(
                    f"Impossible to mint NFT on contract address '{nft_contract}'. Error: {error}",
                )
                sleeping(mode=1)
