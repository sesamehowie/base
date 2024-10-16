import random
from loguru import logger
from datetime import datetime, timedelta
from core.utils.decorators import retry_execution
from core.utils.networks import Network
from requests import Session
from core.clients.evm_client import EvmClient
from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_defunct
from typing import Self
from eth_typing import HexStr
from core.modules.coinbase.coinbase_wallet_mints import Mints


class JuicyAdventure:
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
        self.client = EvmClient(
            account_name=self.account_name,
            private_key=self.private_key,
            network=self.network,
            user_agent=self.user_agent,
            proxy=self.proxy,
        )
        self.mint_data = Mints.JuicyAdventure

        self.default_headers = {"User-Agent": self.user_agent}
        self.default_proxies = {
            "http": f"http://{self.proxy}",
            "https": f"http://{self.proxy}",
        }
        self.mod_val = 11147948505680822770
        self.session = Session()

        self.logger.debug(f"Now working: module {self.mint_data.name}")

    @staticmethod
    def get_random_hex(length):
        characters = "0123456789abcdef"
        return "".join(random.choice(characters) for _ in range(length))

    @staticmethod
    def get_timestamp() -> str:
        return (datetime.now() - timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%S.%f")[
            :-3
        ] + "Z"

    def get_nonce(self) -> str:
        self.logger.info(
            f"{self.account_name} | {self.address} | {self.mint_data.name} | Getting nonce..."
        )
        url = "https://gram.voyage/api/ocs/nonce"

        response = self.session.get(
            url, proxies=self.default_proxies, headers=self.default_headers
        ).json()

        if response["status"] != 200:
            raise

        return response["data"]["nonce"]

    def sign_message(self, nonce: str, timestamp: str) -> str:
        message = f"gram.voyage wants you to sign in with your Ethereum account:\n{self.address}\n\nSign in Grampus.\n\nURI: https://gram.voyage\nVersion: 1\nChain ID: 8453\nNonce: {nonce}\nIssued At: {timestamp}"

        hashable = encode_defunct(text=message)

        signature = Web3.to_hex(
            self.account.sign_message(signable_message=hashable).signature
        )

        return signature

    def get_jwt(self, signature: str, timestamp: str, nonce: str):
        url = "https://gram.voyage/api/ocs/verify"

        payload = {
            "message": {
                "domain": "gram.voyage",
                "address": self.address,
                "statement": "Sign in Grampus.",
                "uri": "https://gram.voyage",
                "version": "1",
                "chainId": self.network.chain_id,
                "nonce": nonce,
                "issuedAt": timestamp,
            },
            "signature": signature,
        }

        response = self.session.post(
            url=url,
            proxies=self.default_proxies,
            json=payload,
            headers=self.default_headers,
        ).json()

        if response["status"] != 200:
            raise

        return response["data"]["token"]

    def get_tx_data(self, jwt_token: str):
        url = "https://gram.voyage/api/ocs/minting"

        session_headers = {
            "User-Agent": self.user_agent,
            "Authorization": f"Bearer {jwt_token}",
        }
        nonce = self.get_random_hex(length=16)
        item_list = list(range(1, 6))

        random_order = random.sample(item_list, 3)

        payload = {
            "address": self.address,
            "nonce": nonce,
            "order": random_order,
        }

        response = self.session.post(
            url, headers=session_headers, proxies=self.default_proxies, json=payload
        ).json()

        if response["status"] != 200:
            raise

        return response["data"]

    def mint_nft(
        self, token_id: int, rarity: int, contr_sig: str | HexStr
    ) -> bool | None:
        from config import JUICY_ADV_ABI, JUICY_ADV_ADDR

        contract = self.client.get_contract(
            contract_addr=JUICY_ADV_ADDR, abi=JUICY_ADV_ABI
        )

        data = contract.encodeABI(
            fn_name="mintJuicyPack", args=[token_id, rarity, contr_sig]
        )

        tx_params = self.client.get_tx_params(
            to_address=JUICY_ADV_ADDR,
            value=0,
            data=data,
            default_gas=Mints.JuicyAdventure.default_gas,
        )

        signed = self.client.sign_transaction(tx_dict=tx_params)

        if signed:
            tx_hash = self.client.send_tx(signed_tx=signed)

            if tx_hash:
                return True

            return False

        return

    @retry_execution
    def run(self) -> bool | None:
        nonce = self.get_nonce()
        timestamp = self.get_timestamp()
        signature = self.sign_message(nonce=nonce, timestamp=timestamp)

        jwt_token = self.get_jwt(signature=signature, timestamp=timestamp, nonce=nonce)

        data = self.get_tx_data(jwt_token=jwt_token)

        token_id = data["tokenId"]
        rarity = data["rarity"]
        sig = data["signature"]

        return self.mint_nft(token_id=token_id, rarity=rarity, contr_sig=sig)
