from module_runner import ModuleRunner
from loguru import logger
import time
import sys
import asyncio


class InvalidIntValueException(Exception):
    pass


async def spinner_task():
    spinner = ["*", "+", "x"]
    idx = 0
    while True:
        sys.stdout.write(f"\rWorking... {spinner[idx]} ")
        sys.stdout.flush()
        idx = (idx + 1) % len(spinner)
        await asyncio.sleep(0.2)


async def main():
    logger.info("Starting run")

    choices = {
        1: "Base Onchain Summer Quest Run",
        2: "Smart Bridge from L2s to Zora and Base",
        3: "Coinbase run and bridge combined",
        4: "OCS campaign results",
        5: "TalentProtocol registration",
    }

    logger.info("Choose action:\n")
    for key, val in choices.items():
        print(f"{key}: {val}")
    print("\n")

    while True:
        try:
            choice = int(input())
            if choice in range(1, 6):
                break
            else:
                raise InvalidIntValueException(
                    "The value you entered is not in range of available tasks!"
                )
        except Exception:
            continue

    spinner = asyncio.create_task(spinner_task())
    start = time.time()
    module_runner = ModuleRunner()

    tasks_mapping = {
        1: module_runner.base_onchain_summer_quest,
        2: module_runner.smart_bridge,
        3: module_runner.smart_coinbase_run,
        4: module_runner.get_and_write_ocs_results,
        5: module_runner.register_talentprotocol,
    }

    tasks = [tasks_mapping[choice]()]
    await asyncio.gather(*tasks)

    spinner.cancel()
    sys.stdout.write("\r")

    end = time.time()

    logger.success(f"Successful run!\n Total runtime: {int(end - start)}s")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.debug("Stopped via Ctrl+C")
