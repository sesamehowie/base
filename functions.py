from eth_typing import HexStr
from core import (
    Relay,
    OKX,
    MintFun,
    Nitro,
    BaseName,
    Deploy,
    TalentProtocol,
    Network,
    Orbiter,
    BaseSwap,
    Aave,
    SushiSwap,
    BalanceChecker,
    StateByNonce,
    EvmClient,
    ProgressCache,
    retry_execution,
)


def withdraw_okx(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    okx = OKX(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return okx.withdraw_native()


def bridge_relay(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
    to_network: Network,
    percentages: tuple[str, str] | None = None,
    amount_range: list[float, float] | None = None,
):
    relay = Relay(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return relay.bridge(
        amount_range=amount_range, percentages=percentages, to_network=to_network
    )


def mint_mintfun(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    mint_fun = MintFun(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return mint_fun.mint()


def mint_base_domain(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = BaseName(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.register()


def bridge_nitro(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
    to_network: Network,
    percentages: tuple[str, str] | None = None,
    amount_range: list[float, float] | None = None,
):
    nitro = Nitro(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return nitro.bridge(
        percentages=percentages, amount_range=amount_range, to_network=to_network
    )


def deploy_random_contract(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    deployer = Deploy(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return deployer.run_deploy()


def register_talentprotocol(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    proxy: str,
):
    talentprotocol = TalentProtocol(
        account_name=account_name,
        private_key=private_key,
        network=network,
        proxy=proxy,
    )

    return talentprotocol.run_register()


def bridge_orbiter(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
    to_network: Network,
    percentages: tuple[str, str] | None = None,
    amount_range: list[float, float] | None = None,
):
    orbiter = Orbiter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return orbiter.bridge(
        to_chain=to_network, percentages=percentages, amount_range=amount_range
    )


def swap_baseswap(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
    from_token: str,
    to_token: str,
    min_amount: float,
    max_amount: float,
    decimal: int,
):
    baseswap = BaseSwap(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return baseswap.swap(
        from_token=from_token,
        to_token=to_token,
        min_amount=min_amount,
        max_amount=max_amount,
        decimal=decimal,
        slippage=3,
        all_amount=False,
        min_percent=35,
        max_percent=50,
    )


def swap_sushiswap(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
    amount_range: list[float, float],
    from_token: str = "ETH",
    to_token: str = "USDC",
):
    sushiswap = SushiSwap(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return sushiswap.swap(
        from_token_name=from_token, to_token_name=to_token, amount_range=amount_range
    )


def deposit_aave(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
    amount_range: list[float, float],
):
    aave = Aave(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return aave.deposit(amount_range=amount_range, make_withdraw=True)


def check_balance(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    checker = BalanceChecker(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return checker.run()


def compare_latest_nonce_to_block(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
    block_num: int,
):
    checker = StateByNonce(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )
    return checker.is_nonce_the_same_on_block(block_num=block_num)


@retry_execution
def save_stats(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
    cache: ProgressCache,
):
    client = EvmClient(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    userdata = client.dump_account_stats()
    address = client.address
    cache.save_stats_to_cache(address=address, userdata=userdata)

    return True


def save_stats_to_file(cache: ProgressCache):
    cache.save_to_file()
