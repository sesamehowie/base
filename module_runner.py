import os
import asyncio
from pyuseragents import random as pyua
import random
from web3 import Web3
from pathlib import Path
from eth_account import Account
from loguru import logger
from core.utils.helpers import sleeping, async_sleeping, write_csv
from core.utils.w3_manager import EthManager
from core.utils.networks import Networks
from core.utils.smart_checker import SmartL2Checker

from functions import *


class ModuleRunner:
    def __init__(self):
        from config import PRIVATE_KEYS, PROXY_CYCLE, ACCOUNT_NAMES

        self.private_keys = PRIVATE_KEYS
        self.proxy_cycle = PROXY_CYCLE
        self.account_names = ACCOUNT_NAMES
        self.logger = logger

    def generate_route_for_the_account(self):
        withdraw_func = withdraw_okx
        relay = bridge_relay

        return (
            withdraw_func,
            relay,
        )

    async def run_account(self, account_name, private_key, user_agent, proxy):
        address = Account.from_key(private_key).address

        self.logger.debug(
            f"Currently working account: {account_name}, address: {address}"
        )

        res_mint = await mint_speedtracer(
            account_name=account_name,
            private_key=private_key,
            network=Networks.Base,
            user_agent=user_agent,
            proxy=proxy,
        )

        print(res_mint)

    async def run_everything(self):
        for key, name in zip(self.private_keys, self.account_names):
            user_agent = pyua()
            proxy = next(self.proxy_cycle)

            res = await self.run_account(
                account_name=name, private_key=key, user_agent=user_agent, proxy=proxy
            )

            print(res)

            sleeping(mode=1)

    async def base_onchain_summer_quest(self):

        # # from settings import RELAY_BRIDGE_AMOUNT_THRESHOLD

        # # random.sample(self.private_keys, len(self.private_keys) // 2)

        # logger.info("Starting Base Onchain Summer Quest Run")
        for key, name in zip(
            self.private_keys,
            self.account_names,
        ):

            user_agent = pyua()
            proxy = next(self.proxy_cycle)

            # client = EthManager(
            #     account_name=name,
            #     private_key=key,
            #     network=Networks.Base,
            #     user_agent=user_agent,
            #     proxy=proxy,
            # )
            # bal = client.get_eth_balance()

            # if bal < Web3.to_wei(0.0003, "ether"):
            #     res_relay = False
            # else:
            res_relay = True

            if not res_relay:
                continue

            else:
                opt_in(name, key, Networks.Base, user_agent, proxy)

                tasks = [mint_truworld_pass]

                # random.shuffle(tasks)

                for task in tasks:

                    if task == mint_speedtracer:

                        task_async = asyncio.create_task(
                            task(name, key, Networks.Base, user_agent, proxy)
                        )

                        await task_async

                    else:

                        task(name, key, Networks.Base, user_agent, proxy)

                    await async_sleeping(1)
                spin_wheel_and_trigger_ref(name, key, Networks.Base, user_agent, proxy)
                check_and_claim_coinbase(name, key, Networks.Base, user_agent, proxy)

            await async_sleeping(2)

    async def smart_bridge(self, key: str, name: str, ua: str, proxy: str):
        logger.info("Starting Bridge to Zora and Base through ETH mainnet")
        client = EthManager(
            account_name=name,
            private_key=key,
            network=Networks.Base,
            user_agent=ua,
            proxy=proxy,
        )

        checker = SmartL2Checker(
            account_name=name,
            private_key=key,
            network=Networks.Base,
            user_agent=ua,
            proxy=proxy,
        )

        network_to_continue = checker.get_runner_network()
        bridges_to_choose_first = [bridge_nitro, bridge_relay]
        rand_item = random.choice(bridges_to_choose_first)

        client.wait_for_gas()

        rand_item(
            account_name=name,
            private_key=key,
            network=network_to_continue,
            user_agent=ua,
            proxy=proxy,
            percentages=("97", "98"),
            to_network=Networks.Ethereum,
        )

        f_percent = ("39", "42")
        s_percent = ("85", "87")

        client.wait_for_gas()

        selection_items = ["Zora", "Base"]

        for _ in range(random.randint(1, 5)):
            random.shuffle(selection_items)

        first_item, second_item = selection_items

        if first_item == "Zora":
            zora_instant_bridge(
                account_name=name,
                private_key=key,
                network=Networks.Ethereum,
                user_agent=ua,
                proxy=proxy,
                percentages=f_percent,
            )
            bridges_to_choose = [bridge_nitro, bridge_relay]

            bridge_base = random.choice(bridges_to_choose)

            bridge_base(
                account_name=name,
                private_key=key,
                network=Networks.Ethereum,
                user_agent=ua,
                proxy=proxy,
                percentages=s_percent,
                to_network=Networks.Base,
            )
        else:
            bridges_to_choose = [bridge_nitro, bridge_relay]

            bridge_base = random.choice(bridges_to_choose)

            bridge_base(
                account_name=name,
                private_key=key,
                network=Networks.Ethereum,
                user_agent=ua,
                proxy=proxy,
                percentages=f_percent,
                to_network=Networks.Base,
            )

            zora_instant_bridge(
                account_name=name,
                private_key=key,
                network=Networks.Ethereum,
                user_agent=ua,
                proxy=proxy,
                percentages=s_percent,
            )

        sleeping(1)

    async def smart_coinbase_run(self):
        self.logger.info("Starting smart run...")

        for key, name in list(zip(self.private_keys, self.account_names)):
            ua = pyua()
            proxy = next(self.proxy_cycle)

            eth_client = EthManager(name, key, Networks.Ethereum, ua, proxy)
            zora_client = EthManager(name, key, Networks.Zora, ua, proxy)

            bal_eth = eth_client.get_eth_balance()
            bal_zora = zora_client.get_eth_balance()

            if bal_eth >= Web3.to_wei(0.008, "ether"):
                f_percent = ("39", "42")
                s_percent = ("85", "87")

                eth_client.wait_for_gas()

                bridges_to_choose = [bridge_nitro, bridge_relay]

                bridge_base = random.choice(bridges_to_choose)

                bridge_base(
                    account_name=name,
                    private_key=key,
                    network=Networks.Ethereum,
                    user_agent=ua,
                    proxy=proxy,
                    percentages=f_percent,
                    to_network=Networks.Base,
                )

                zora_instant_bridge(
                    account_name=name,
                    private_key=key,
                    network=Networks.Ethereum,
                    user_agent=ua,
                    proxy=proxy,
                    percentages=s_percent,
                )
            elif Web3.to_wei(0.004, "ether") <= bal_eth <= Web3.to_wei(0.006, "ether"):
                percentage = ("85", "87")

                if bal_zora <= Web3.to_wei(0.002, "ether"):
                    zora_instant_bridge(
                        account_name=name,
                        private_key=key,
                        network=Networks.Ethereum,
                        user_agent=ua,
                        proxy=proxy,
                        percentages=percentage,
                    )
                else:
                    bridge_relay(
                        account_name=name,
                        private_key=key,
                        network=Networks.Ethereum,
                        user_agent=ua,
                        proxy=proxy,
                        percentages=percentage,
                        to_network=Networks.Base,
                    )
            else:
                await self.smart_bridge(key, name, ua, proxy)

    async def get_and_write_ocs_results(self):
        from config import WORKING_DIR

        self.logger.info("Starting point checker for OCS campaign...")
        results = []

        for key, name in list(zip(self.private_keys, self.account_names)):
            ua = pyua()
            proxy = next(self.proxy_cycle)

            while True:
                res = get_ocs_campaign_result(
                    account_name=name,
                    private_key=key,
                    network=Networks.Base,
                    user_agent=ua,
                    proxy=proxy,
                )

                if isinstance(res, list):
                    results.append(res)
                    break

            await async_sleeping(1)
        output_path = os.path.join(WORKING_DIR, Path("data/results/points.csv"))

        write_csv(file_name=output_path, data=results)

    async def register_talentprotocol(self):
        self.logger.info("Starting Talent Protocol registration run...")

        for key, name in list(zip(self.private_keys, self.account_names)):

            proxy = next(self.proxy_cycle)

            address = Account.from_key(key).address

            res = register_talentprotocol(
                account_name=name, private_key=key, network=Networks.Base, proxy=proxy
            )

            self.logger.info(f"{address} - result: {res}")

            await async_sleeping(2)