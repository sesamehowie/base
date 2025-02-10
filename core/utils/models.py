from dataclasses import dataclass
from eth_typing import ChecksumAddress


@dataclass
class AccountStats:
    address: str | ChecksumAddress
    tx_count: int
    eth_balance: int | float
    last_tx_timestamp: int

    def to_dict(self):
        return {
            "address": self.address,
            "txCount": self.tx_count,
            "ethBalance": self.eth_balance,
            "lastTransaction": self.last_tx_timestamp,
        }
