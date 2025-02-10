from eth_typing import ChecksumAddress
from core.utils.models import AccountStats
from core.utils.helpers import write_json
from config import ACCOUNT_STATS_FILE_LOCATION


class ProgressCache:
    def __init__(self):
        self.address_book = []
        self.kv_storage = dict()

    def save_stats_to_cache(
        self, address: str | ChecksumAddress, userdata: AccountStats
    ) -> None:
        if address not in self.address_book:
            self.address_book.append(address)
        self.kv_storage.update({address: userdata.to_dict()})

    def save_to_file(self) -> None:
        write_json(file_name=ACCOUNT_STATS_FILE_LOCATION, data=self.kv_storage)
