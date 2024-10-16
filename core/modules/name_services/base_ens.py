from typing import Self
import random
from eth_account import Account
from core.clients.evm_client import EvmClient
from web3 import Web3
from requests import Session
from eth_typing import HexStr
from loguru import logger
from core.utils.networks import Network
from core.utils.decorators import retry_execution
from config import ENS_ABI, REGISTRY_CONTROLLER_ADDR
from core.modules.coinbase.coinbase_wallet_mints import Mints
from hexbytes import HexBytes
from eth_utils import keccak, to_hex
from eth_abi import encode


class BaseName:
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
        self.session = Session()
        self.client = EvmClient(
            account_name=self.account_name,
            private_key=self.private_key,
            network=self.network,
            user_agent=self.user_agent,
            proxy=self.proxy,
        )
        self.registry_contract = self.client.get_contract(
            contract_addr=REGISTRY_CONTROLLER_ADDR, abi=ENS_ABI
        )
        self.default_headers = {"User-Agent": self.user_agent}
        self.default_proxies = {
            "http": f"http://{self.proxy}",
            "https": f"http://{self.proxy}",
        }
        self.module_name = "Base.eth Domain Name"

        self.logger.debug(f"Now working: module {self.module_name}")

    @staticmethod
    def namehash(name):
        node = HexBytes("0x" + "00" * 32)
        if name:
            labels = name.split(".")
            for label in reversed(labels):
                label_hash = keccak(text=label)
                node = keccak(node + label_hash)
        return node

    @retry_execution
    def get_five_letter_words(self) -> list[str]:
        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Searching for 5 letter words..."
        )

        words = []

        url = "https://fly.wordfinderapi.com/api/search"

        payload = {
            "length": random.randint(5, 8),
            "page_token": random.randint(1, 5),
            "page_size": 100,
            "word_sorting": "points",
            "dictionary": "all_en",
        }

        self.session.headers.update({"User-Agent": self.user_agent})

        response = self.session.get(
            url=url, proxies=self.default_proxies, params=payload, timeout=60
        ).json()

        for word_page in response["word_pages"]:
            for item in word_page["word_list"]:
                word = item.get("word", None)
                if word:
                    words.append(word)

        return words

    @retry_execution
    def get_name_suggestion(self, word: str):
        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Getting name suggestions from Base..."
        )

        self.session.headers.update({"User-Agent": self.user_agent})

        url = f"https://www.base.org/api/name/{word}"

        response = self.session.get(url, proxies=self.default_proxies).json()

        return random.choice(response["suggestion"])

    @retry_execution
    def register(self):
        is_registered = self.registry_contract.functions.discountedRegistrants(
            self.address
        ).call()

        if is_registered:
            self.logger.warning(
                f"{self.account_name} | {self.address} | {self.module_name} | This wallet has already registered for a name."
            )
            return False
        word = random.choice(self.get_five_letter_words())

        name = self.get_name_suggestion(word)
        name2 = name + ".base.eth"

        available = self.registry_contract.functions.available(name).call()
        if available:
            logger.info(
                f"{self.account_name} | {self.address} | {self.module_name} | Starting mint of name on Base..."
            )
        else:
            raise

        tx_params = {
            "from": self.address,
            "nonce": self.client.w3.eth.get_transaction_count(self.address),
        }

        name_hash = self.namehash(name2)
        payload = to_hex(encode(["bytes32", "string"], [name_hash, name2]))

        data = [
            Web3.to_bytes(
                hexstr=f"0xd5fa2b00{Web3.to_hex(name_hash)[2:]}000000000000000000000000{self.address.lower()[2:]}"
            ),
            Web3.to_bytes(hexstr=f"0x77372213{payload[2:]}"),
        ]

        request = (
            name,
            self.address,
            31557600,
            Web3.to_checksum_address("0xC6d566A56A1aFf6508b41f6c90ff131615583BCD"),
            data,
            True,
        )

        txn = self.registry_contract.functions.discountedRegister(
            request,
            Web3.to_bytes(
                hexstr="0xc1af3c32616941d3f6d85f4f01aafb556b5620e8868acac1ed2a816fb9d0676d"
            ),
            Web3.to_bytes(hexstr="0x00"),
        ).build_transaction(tx_params)

        try:
            txn["gas"] = self.client.w3.eth.estimate_gas(transaction=txn)
        except Exception:
            txn["gas"] = Mints.BaseEns.default_gas

        signed = self.client.sign_transaction(tx_dict=txn)

        if signed:
            tx_hash = self.client.send_tx(signed_tx=signed)

            if tx_hash:
                return True

            return False

        return
