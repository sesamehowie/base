import random
from pathlib import Path
import json
import os
from web3 import Web3
from itertools import cycle
from core.utils.helpers import read_txt, decipher
from core.utils.proxy_checker import rule_out_faulty_proxies
from settings import SHUFFLE_KEYS, SHUFFLE_PROXIES

WORKING_DIR = Path(os.getcwd())

RELAY_CHAIN_NAME = {
    42161: "Arbitrum",
    8453: "Base",
    10: "Optimism",
    7777777: "Zora",
    1: "Ethereum",
}

REGISTRY_CONTROLLER_ADDR = Web3.to_checksum_address(
    "0x4cCb0BB02FCABA27e82a56646E81d8c5bC4119a5"
)
JUICY_ADV_ADDR = Web3.to_checksum_address("0x6ba5Ba71810c1196f20123B57B66C9ed2A5dBd76")

# ABI instantiation
AAVE_ABI = json.load(open(os.path.join(WORKING_DIR, Path("data/abis/aave.json"))))
ERC20_ABI = json.load(open(os.path.join(WORKING_DIR, Path("data/abis/erc20.json"))))
BUILDERS_ABI = json.load(
    open(os.path.join(WORKING_DIR, Path("data/abis/builders.json")))
)
SEED_TOKEN_ABI = json.load(
    open(os.path.join(WORKING_DIR, Path("data/abis/seed_abi.json")))
)
SEED_ROUTER_ABI = json.load(
    open(os.path.join(WORKING_DIR, Path("data/abis/seed_router.json")))
)
SEED_MINTER_ABI = json.load(
    open(os.path.join(WORKING_DIR, Path("data/abis/seed_minter.json")))
)
ZORA_MINTER_ABI = json.load(
    open(os.path.join(WORKING_DIR, Path("data/abis/zora_minter.json")))
)
BASE_NFT_ABI = json.load(
    open(os.path.join(WORKING_DIR, Path("data/abis/base_nft.json")))
)
STIX_ABI = json.load(open(os.path.join(WORKING_DIR, Path("data/abis/stix.json"))))
EXECUTOR_ABI = json.load(
    open(os.path.join(WORKING_DIR, Path("data/abis/executor.json")))
)
CLAIMABLE_ABI = json.load(
    open(os.path.join(WORKING_DIR, Path("data/abis/claimable.json")))
)
MIGGLES_ABI = json.load(open(os.path.join(WORKING_DIR, Path("data/abis/miggles.json"))))
ENS_ABI = json.load(open(os.path.join(WORKING_DIR, Path("data/abis/base_ens.json"))))
JUICY_ADV_ABI = json.load(
    open(os.path.join(WORKING_DIR, Path("data/abis/juicy_adventure.json")))
)
ZORA_BASE_1155_ABI = json.load(
    open(os.path.join(WORKING_DIR, Path("data/abis/zora_1155_base.json")))
)
STORAGE_ABI = json.load(open(os.path.join(WORKING_DIR, Path("data/abis/storage.json"))))
OWNER_ABI = json.load(open(os.path.join(WORKING_DIR, Path("data/abis/owner.json"))))
VOTER_ABI = json.load(open(os.path.join(WORKING_DIR, Path("data/abis/voter.json"))))
BASESWAP_ROUTER_ABI = json.load(
    open(os.path.join(WORKING_DIR, Path("data/abis/baseswap_router.json")))
)

# Worker info serialization
PRIVATE_KEYS = [
    decipher(item)
    for item in read_txt(os.path.join(WORKING_DIR, Path("data/private_keys.txt")))
]

if SHUFFLE_KEYS:
    random.shuffle(PRIVATE_KEYS)


ACCOUNT_NAMES = tuple([i for i in range(1, len(PRIVATE_KEYS) + 1)])

PROXY_INPUTS = read_txt(os.path.join(WORKING_DIR, Path("data/proxies.txt")))

WORKING_PROXIES = rule_out_faulty_proxies(PROXY_INPUTS)

if SHUFFLE_PROXIES:
    random.shuffle(WORKING_PROXIES)

PROXY_CYCLE = cycle(WORKING_PROXIES)

AAVE_CONTRACT = "0x18cd499e3d7ed42feba981ac9236a278e4cdc2ee"

AAVE_WETH_CONTRACT = "0xD4a0e0b9149BCee3C920d2E00b5dE09138fd8bb7"

SEED_SWAPPER_ADDR = Web3.to_checksum_address(
    "0x327df1e6de05895d2ab08513aadd9313fe505d86"
)
SEED_TOKEN_ADDR = Web3.to_checksum_address("0x546d239032b24eceee0cb05c92fc39090846adc7")
SEED_MINTER_ADDR = Web3.to_checksum_address(
    "0xeb4e16c804AE9275a655AbBc20cD0658A91F9235"
)
BASE_ETH_MASK = Web3.to_checksum_address("0x4200000000000000000000000000000000000006")
SEED_INF_APPROVE_AMT = (
    115792089237316195423570985008687907853269984665640564039457584007913129639935
)
CITYVERSE_CONTRACT_ADDR = Web3.to_checksum_address(
    "0x2E2c0753fc81BE22381c674ADD7A05F24cfD9761"
)
CITYVERSE_PUBLIC_MINT_CALLDATA = (
    "0x2db115440000000000000000000000000000000000000000000000000000000000000001"
)

OKX_CHAIN_NATIVE_MAPPING = {
    "Arbitrum": "ETH-Arbitrum One",
    "Optimism": "ETH-Optimism",
    "Base": "ETH-Base",
    "Ethereum Mainnet": "ETH-ERC20",
}

OKX_SIGNIFICANT_DECIMALS = {
    "ETH-Arbitrum One": 4,
    "ETH-Optimism": 4,
    "ETH-Base": 4,
    "ETH-ERC20": 4,
}

OKX_FEES = {
    "Arbitrum": 0.0001,
    "Optimism": 0.00004,
    "Base": 0.00004,
    "Ethereum Mainnet": 0.0009,
}

CHAIN_IDS = {
    "Ethereum Mainnet": 1,
    "Zora": 7777777,
    "Base": 8453,
    "Optimism": 10,
    "Arbitrum": 42161,
}

BASE_TOKENS = {
    "ETH": "0x4200000000000000000000000000000000000006",
    "WETH": "0x4200000000000000000000000000000000000006",
    "USDBC": "0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA",
    "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "DAI": "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb",
}

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
ZERO_PROOF = Web3.to_bytes(
    hexstr="0x00000000000000000000000000000000000000000000000000000000000000000000000000000000"
)


MINTFUN_CONTRACTS = [
    "0x7AD0adfF258490973646f1c6ef5A5AAecae8B471",
    "0x1973CeF74250aeBAbE7C4d038670D71593d1BEA8",
    "0x170d97A67119D82F617F7f824ea6952BcE14ce62",
    "0x67F3D0d6BD65b2352Cc8fA781D55c24F7C81aD0c",
    "0x9Da3002624977A7c76A0B37122b80cE412F54036",
    "0x624C1e3FCc7c2eBB86C765F3D4C92961FF6B93ab",
    "0x0e3270feAfDaDB0FEa521f8B8c8B001De228D063",
    "0xA6B2F024d961aFc5B524e7c7C850199083372240",
    "0x5d2939411fC0252F4257604674cEd8D97581B9eA",
    "0xEF6366C647750F813bD0675F5ee06648D4d82b36",
]

MINTFUN_ABI = {
    1: [
        {
            "inputs": [
                {"internalType": "uint32", "name": "quantity", "type": "uint32"}
            ],
            "name": "mint",
            "outputs": [],
            "stateMutability": "payable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "name",
            "outputs": [{"internalType": "string", "name": "", "type": "string"}],
            "stateMutability": "view",
            "type": "function",
        },
    ],
    2: [
        {
            "inputs": [
                {"internalType": "address", "name": "minter", "type": "address"}
            ],
            "name": "mint",
            "outputs": [],
            "stateMutability": "payable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "name",
            "outputs": [{"internalType": "string", "name": "", "type": "string"}],
            "stateMutability": "view",
            "type": "function",
        },
    ],
    3: [],
    4: [
        {
            "inputs": [],
            "name": "mint",
            "outputs": [],
            "stateMutability": "payable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "name",
            "outputs": [{"internalType": "string", "name": "", "type": "string"}],
            "stateMutability": "view",
            "type": "function",
        },
    ],
}

ETH_MASK = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"

BASESWAP_CONTRACTS = {"router": "0x327Df1E6de05895d2ab08513aaDD9313Fe505d86"}
