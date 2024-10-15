from typing import Self
from eth_account import Account
from core.utils.w3_manager import EthManager
from web3 import Web3
import requests
from eth_typing import HexStr
from loguru import logger
from dataclasses import dataclass
from core.utils.networks import Network
from core.utils.custom_wrappers import exception_handler_with_retry


class Badge:
    def __init__(self, name: str, badge_id: int | str):
        self.name = name
        self.badge_id = badge_id if isinstance(badge_id, str) else str(badge_id)


@dataclass
class Badges:
    StandWithCrypto = Badge(name="Stand With Crypto", badge_id="1")
    CoinbaseOne = Badge(name="Coinbase One", badge_id="2")
    Builder = Badge(name="Builder", badge_id="3")
    Collector = Badge(name="Collector", badge_id="4")
    Trader = Badge(name="Trader", badge_id="5")
    Saver = Badge(name="Saver", badge_id="6")
    Based10Tx = Badge(name="Based(10 transactions)", badge_id="7")
    Based50Tx = Badge(name="Based(50 transactions)", badge_id="8")
    Based100Tx = Badge(name="Based(100 transactions)", badge_id="9")
    Based1000Tx = Badge(name="Based(1000 transactions)", badge_id="10")

    All = [
        StandWithCrypto,
        CoinbaseOne,
        Builder,
        Collector,
        Trader,
        Saver,
        Based10Tx,
        Based50Tx,
        Based100Tx,
        Based1000Tx,
    ]


class BadgeClaimer:
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
        self.client = EthManager(
            account_name=self.account_name,
            private_key=self.private_key,
            network=self.network,
            user_agent=self.user_agent,
            proxy=self.proxy,
        )
        self.module_name = "BadgeClaimer"

        self.logger.debug(f"Now working: module {self.module_name}")

    def mint(self):
        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Starting mint..."
        )

        to_addr = Web3.to_checksum_address("0x0c45CA58cfA181b038E06dd65EAbBD1a68d3CcF3")
        data = f"0x84bb1e42000000000000000000000000{self.address.lower()[2:]}0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee00000000000000000000000000000000000000000000000000005af3107a400000000000000000000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000001800000000000000000000000000000000000000000000000000000000000000080ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff00000000000000000000000000000000000000000000000000005af3107a4000000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
        value = 100000000000000

        tx_params = self.client.get_tx_params(
            to_address=to_addr, data=data, value=value, default_gas=150000
        )

        signed = self.client.sign_transaction(tx_dict=tx_params)

        if signed:
            tx_hash = self.client.send_tx(signed_tx=signed)

            if tx_hash:
                return True

            return False

        return

    def claim_badge(self, badge: Badge):
        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Trying to claim {badge.name} badge..."
        )

        url = "https://basehunt.xyz/api/badges/claim"

        headers = {"User-Agent": self.user_agent}

        proxies = {"http": f"http://{self.proxy}", "https": f"http://{self.proxy}"}

        req_body = {"badgeId": badge.badge_id, "gameId": 2, "userAddress": self.address}

        response = requests.post(
            url=url, headers=headers, json=req_body, proxies=proxies
        )

        data = response.json()

        if data["success"] is True:
            res = True
        else:
            res = False

        (
            self.logger.success(
                f"{self.account_name} | {self.address} | {self.module_name} | Badge Claimed!"
            )
            if res is True
            else self.logger.warning(
                f"{self.account_name} | {self.address} | {self.module_name} | Badge not claimed."
            )
        )

        return res

    def claim_badges(self):

        for badge in Badges.All:

            if badge == Badges.Builder:

                res = self.claim_badge(badge=badge)
                if not res:
                    self.mint()
                    self.claim_badge(badge=badge)
            else:
                self.claim_badge(badge=badge)

        return True

    @exception_handler_with_retry
    def run(self):
        run_res = self.claim_badges()

        if run_res:
            return True

        return
