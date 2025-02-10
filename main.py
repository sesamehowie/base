import os
import time
import random
import pyuseragents

from pathlib import Path
from loguru import logger
from pyfiglet import Figlet
from concurrent.futures import ThreadPoolExecutor
from core.utils.state_by_nonce import StateByNonce
from core.utils.helpers import read_txt, write_txt

from functions import (
    withdraw_okx,
    bridge_relay,
    bridge_nitro,
    register_talentprotocol,
    bridge_orbiter,
    swap_baseswap,
    deploy_random_contract,
    swap_sushiswap,
    deposit_aave,
)

from core import Networks, sleeping

from settings import (
    OKX_WITHDRAW_CHAIN_ID,
    RELAY_DEST_CHAIN_ID,
    RELAY_AMT_RANGE,
    NITRO_AMT_RANGE,
    ORBITER_AMT_RANGE,
    ORBITER_TO_CHAIN_ID,
    BASESWAP_AMT_RANGE,
    BASESWAP_FROM_TOKEN,
    BASESWAP_TO_TOKEN,
    SUSHISWAP_AMT_RANGE,
    SUSHISWAP_FROM_TOKEN,
    SUSHISWAP_TO_TOKEN,
    AAVE_AMT_RANGE,
    SHUFFLE_KEYS,
    THREAD_DELAY,
)

from config import ACCOUNT_NAMES, PRIVATE_KEYS, PROXIES

MODULES = {
    1: ("OKX Withdraw", withdraw_okx),
    2: ("Relay bridge", bridge_relay),
    3: ("Nitro bridge", bridge_nitro),
    4: ("Register Talentprotocol", register_talentprotocol),
    5: ("Orbiter bridge", bridge_orbiter),
    6: ("Swap on BaseSwap", swap_baseswap),
    7: ("Deploy random contract", deploy_random_contract),
    8: ("Swap on Sushiswap", swap_sushiswap),
    9: ("Deposit and withdraw on Aave", deposit_aave),
    10: ("Random module", "random"),
}


DAILY_MODULE_IDS = [6, 7, 8, 9]


def ask_module() -> int:
    print("What module would you like to execute:\n\n")

    for k, v in MODULES.items():
        print(f"{k}. {v[0]}")

    print("\n")
    res = int(input())

    return res


def delay_wrapper(
    account_name: str | int,
    private_key: str,
    proxy: str,
    module_choice: str,
    thread_num: int,
) -> None:
    if thread_num > 1:
        t = random.randint(*THREAD_DELAY)
        logger.info(f"Starting thread {account_name} with delay {t} seconds")
        time.sleep(t)
    execute_module(account_name, private_key, proxy, module_choice)


def execute_module(
    account_name: str | int, private_key: str, proxy: str, module_choice: int
) -> bool:

    arguments = prepare_args_for_module(
        account_name=account_name,
        private_key=private_key,
        proxy=proxy,
        module_choice=module_choice,
    )

    res = MODULES[module_choice][1](*arguments)
    sleeping(2)
    return True if res else False


def check_work() -> bool:
    cwd = os.getcwd()
    keys = PRIVATE_KEYS
    proxies = PROXIES
    account_names = ACCOUNT_NAMES

    idle_wallets = []

    if SHUFFLE_KEYS:
        combined_items = list(zip(keys, proxies))
        random.shuffle(combined_items)
        keys, proxies = zip(*combined_items)

    for account_name, private_key, proxy in zip(
        account_names,
        keys,
        proxies,
    ):
        ua = pyuseragents.random()
        client = StateByNonce(
            account_name=account_name,
            private_key=private_key,
            network=Networks.Base,
            user_agent=ua,
            proxy=proxy,
        )
        block = 25328846

        res = client.is_nonce_the_same_on_block(block)
        if res:
            idle_wallets.append(client.address)
        sleeping(1)

    if idle_wallets:
        keys_filepath = os.path.join(cwd, Path("data/private_keys.txt"))

        item_list = []
        items = read_txt(keys_filepath)

        for result in idle_wallets:
            for item in items:
                if result in item:
                    item_list.append(item)
                else:
                    continue

        write_txt(keys_filepath, item_list, "w")

    return True


def prepare_args_for_module(
    account_name: str | int, private_key: str, proxy: str, module_choice: int
) -> list:
    user_agent = pyuseragents.random()

    module_args = {
        1: [
            account_name,
            private_key,
            Networks.get_network_by_chain_id(chain_id=OKX_WITHDRAW_CHAIN_ID),
            user_agent,
            proxy,
        ],
        2: [
            account_name,
            private_key,
            Networks.Base,
            user_agent,
            proxy,
            RELAY_DEST_CHAIN_ID,
            None,
            RELAY_AMT_RANGE,
        ],
        3: [
            account_name,
            private_key,
            Networks.Base,
            user_agent,
            proxy,
            Networks.Zora,
            None,
            NITRO_AMT_RANGE,
        ],
        4: [account_name, private_key, Networks.Base, proxy],
        5: [
            account_name,
            private_key,
            Networks.Base,
            user_agent,
            proxy,
            Networks.get_network_by_chain_id(ORBITER_TO_CHAIN_ID),
            None,
            ORBITER_AMT_RANGE,
        ],
        6: [
            account_name,
            private_key,
            Networks.Base,
            user_agent,
            proxy,
            BASESWAP_FROM_TOKEN,
            BASESWAP_TO_TOKEN,
            BASESWAP_AMT_RANGE[0],
            BASESWAP_AMT_RANGE[1],
            18,
        ],
        7: [account_name, private_key, Networks.Base, user_agent, proxy],
        8: [
            account_name,
            private_key,
            Networks.Base,
            user_agent,
            proxy,
            SUSHISWAP_AMT_RANGE,
            SUSHISWAP_FROM_TOKEN,
            SUSHISWAP_TO_TOKEN,
        ],
        9: [
            account_name,
            private_key,
            Networks.Base,
            user_agent,
            proxy,
            AAVE_AMT_RANGE,
        ],
    }

    return module_args[module_choice]


def main() -> None:
    keys = PRIVATE_KEYS
    proxies = PROXIES
    account_names = ACCOUNT_NAMES
    choice = ask_module()

    if choice == 10:
        choices = [random.choice(DAILY_MODULE_IDS) for _ in keys]
    else:
        choices = [choice for _ in keys]

    if SHUFFLE_KEYS:
        combined_items = list(zip(keys, proxies))
        random.shuffle(combined_items)
        keys, proxies = zip(*combined_items)

    threads = int(input("Enter number of threads: \n"))

    print("Starting...\n")

    if threads == 1:
        for account_name, private_key, proxy, module_choice in zip(
            account_names, keys, proxies, choices
        ):
            delay_wrapper(account_name, private_key, proxy, module_choice, thread_num=1)
    else:
        thread_iterable = [threads] * len(keys)
        with ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(
                lambda args: delay_wrapper(*args),
                zip(account_names, keys, proxies, choices, thread_iterable),
            )


if __name__ == "__main__":
    f = Figlet(font="slant")
    word = "amogus"
    print(f.renderText(word))

    main()
