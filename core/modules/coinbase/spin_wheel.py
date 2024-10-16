from loguru import logger
from core.utils.decorators import retry_execution
from core.utils.networks import Network
from core.utils.helpers import sleeping
from core.clients.evm_client import EvmClient
import requests
from web3 import Web3
from eth_account import Account
from typing import Self
from eth_typing import HexStr
from settings import COINBASE_REFERRAL_UUID


class FailedSpinWarning(Exception):
    pass


class SpinWheel:
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
        self.module_name = "SpinWheel"

        self.logger.debug(f"Now working: module {self.module_name}")

    @retry_execution
    def opt_in(self) -> bool | None:

        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Triggering referral..."
        )

        url = "https://basehunt.xyz/api/profile/opt-in"

        headers = {"User-Agent": self.user_agent}

        proxies = {"http": f"http://{self.proxy}", "https": f"http://{self.proxy}"}

        req_body = {
            "gameId": 2,
            "referralId": COINBASE_REFERRAL_UUID,
            "userAddress": self.address,
        }

        response = requests.post(
            url=url, headers=headers, json=req_body, proxies=proxies
        )

        if response.status_code == 200:
            self.logger.success(
                f"{self.account_name} | {self.address} | {self.module_name} | Referral done!"
            )

            return True
        self.logger.warning(
            f"{self.account_name} | {self.address} | {self.module_name} | Request has {response.status_code} code, needed 200..."
        )

        return

    @retry_execution
    def trigger_probs(self) -> bool | None:
        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Checking available spin..."
        )

        url = f"https://basehunt.xyz/api/spin-the-wheel?gameId=2&userAddress={self.address}"

        headers = {"User-Agent": self.user_agent}

        proxies = {"http": f"http://{self.proxy}", "https": f"http://{self.proxy}"}

        response = requests.get(url=url, headers=headers, proxies=proxies)

        if response.status_code == 200:
            data = response.json()
            return True if data["spinData"]["hasAvailableSpin"] else False

        return

    @retry_execution
    def execute_spin(self) -> bool | None:
        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Executing spin..."
        )

        url = "https://basehunt.xyz/api/spin-the-wheel/execute"

        req_body = {"gameId": "2", "userAddress": self.address}

        headers = {"User-Agent": self.user_agent}

        proxies = {"http": f"http://{self.proxy}", "https": f"http://{self.proxy}"}

        response = requests.post(
            url=url, json=req_body, headers=headers, proxies=proxies, timeout=60
        )
        if response.status_code == 200:
            data = response.json()
            if not data["spinData"]["hasAvailableSpin"]:
                points = data["spinData"]["lastSpinResult"]["points"]
                self.logger.success(
                    f"{self.account_name} | {self.address} | {self.module_name} | Spin successful! Got {points} points!"
                )
                return True
        elif response.status_code == 400:
            logger.warning(
                f"{self.account_name} | {self.address} | {self.module_name} | This account does not have enough points to be able to spin..."
            )
            return True
        else:

            self.logger.warning(
                f"{self.account_name} | {self.address} | {self.module_name} | Spin didnt come through"
            )

            raise FailedSpinWarning(
                f"Spin didnt come through for address {self.address}"
            )

        return

    def run_daily_spin(self) -> bool | None:
        spin_available = self.trigger_probs()
        if spin_available:

            while spin_available:
                try:
                    res = self.execute_spin()

                    if res is not None:
                        return res
                except Exception as e:
                    print(e)
                    sleeping(1)

            return False
