from dataclasses import dataclass


class Network:

    def __init__(
        self,
        name,
        chain_id,
        rpc_list,
        scanner,
        eip1559_support: bool = False,
        token: str = "ETH",
    ):
        self.name = name
        self.chain_id = chain_id
        self.rpc_list = rpc_list
        self.scanner = scanner
        self.token = token


@dataclass
class Networks:
    Ethereum = Network(
        name="Ethereum Mainnet",
        chain_id=1,
        rpc_list=[
            "https://eth.meowrpc.com",
            "https://eth.drpc.org",
        ],
        scanner="https://etherscan.io",
        eip1559_support=True,
    )
    Base = Network(
        name="Base",
        chain_id=8453,
        rpc_list=[
            "https://base.meowrpc.com",
            "https://1rpc.io/base",
        ],
        scanner="https://basescan.org",
        eip1559_support=True,
    )
    Optimism = Network(
        name="Optimism",
        rpc_list=[
            "https://rpc.ankr.com/optimism/",
            "https://optimism.drpc.org",
            "https://1rpc.io/op",
        ],
        chain_id=10,
        eip1559_support=True,
        token="ETH",
        scanner="https://optimistic.etherscan.io",
    )
    Linea = Network(
        name="Linea",
        rpc_list=[
            "https://rpc.linea.build",
            "https://1rpc.io/linea",
            "https://linea.blockpi.network/v1/rpc/public",
        ],
        chain_id=59144,
        eip1559_support=False,
        token="ETH",
        scanner="https://lineascan.build",
    )
    Arbitrum = Network(
        name="Arbitrum",
        rpc_list=[
            "https://arbitrum.meowrpc.com",
            "https://arbitrum-one.publicnode.com",
        ],
        chain_id=42161,
        eip1559_support=True,
        token="ETH",
        scanner="https://arbiscan.io/",
    )
    Zora = Network(
        name="Zora",
        chain_id=7777777,
        rpc_list=["https://rpc.zora.energy"],
        scanner="https://explorer.zora.energy",
        eip1559_support=True,
        token="ETH",
    )
