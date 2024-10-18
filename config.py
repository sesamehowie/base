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
SUSHISWAP_CONTRACTS = {
    "Base": {
        "router": "0xFB7eF66a7e61224DD6FcD0D7d9C3be5C8B049b9f",
        "quoter": "0xb1E835Dc2785b52265711e17fCCb0fd018226a6e",
    },
    "Arbitrum Nova": {
        "router": "0xc14Ee6B248787847527e11b8d7Cf257b212f7a9F",
        "quoter": "0xb1E835Dc2785b52265711e17fCCb0fd018226a6e",
    },
    "Scroll": {
        "router": "0x33d91116e0370970444B0281AB117e161fEbFcdD",
        "quoter": "0xe43ca1Dee3F0fc1e2df73A0745674545F11A59F5",
    },
}

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

SUSHISWAP_ABI = {
    "router": [
        {
            "inputs": [
                {"internalType": "address", "name": "_factory", "type": "address"},
                {"internalType": "address", "name": "_WETH9", "type": "address"},
            ],
            "stateMutability": "nonpayable",
            "type": "constructor",
        },
        {
            "inputs": [],
            "name": "WETH9",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "components": [
                        {"internalType": "bytes", "name": "path", "type": "bytes"},
                        {
                            "internalType": "address",
                            "name": "recipient",
                            "type": "address",
                        },
                        {
                            "internalType": "uint256",
                            "name": "deadline",
                            "type": "uint256",
                        },
                        {
                            "internalType": "uint256",
                            "name": "amountIn",
                            "type": "uint256",
                        },
                        {
                            "internalType": "uint256",
                            "name": "amountOutMinimum",
                            "type": "uint256",
                        },
                    ],
                    "internalType": "struct ISwapRouter.ExactInputParams",
                    "name": "params",
                    "type": "tuple",
                }
            ],
            "name": "exactInput",
            "outputs": [
                {"internalType": "uint256", "name": "amountOut", "type": "uint256"}
            ],
            "stateMutability": "payable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "components": [
                        {
                            "internalType": "address",
                            "name": "tokenIn",
                            "type": "address",
                        },
                        {
                            "internalType": "address",
                            "name": "tokenOut",
                            "type": "address",
                        },
                        {"internalType": "uint24", "name": "fee", "type": "uint24"},
                        {
                            "internalType": "address",
                            "name": "recipient",
                            "type": "address",
                        },
                        {
                            "internalType": "uint256",
                            "name": "deadline",
                            "type": "uint256",
                        },
                        {
                            "internalType": "uint256",
                            "name": "amountIn",
                            "type": "uint256",
                        },
                        {
                            "internalType": "uint256",
                            "name": "amountOutMinimum",
                            "type": "uint256",
                        },
                        {
                            "internalType": "uint160",
                            "name": "sqrtPriceLimitX96",
                            "type": "uint160",
                        },
                    ],
                    "internalType": "struct ISwapRouter.ExactInputSingleParams",
                    "name": "params",
                    "type": "tuple",
                }
            ],
            "name": "exactInputSingle",
            "outputs": [
                {"internalType": "uint256", "name": "amountOut", "type": "uint256"}
            ],
            "stateMutability": "payable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "components": [
                        {"internalType": "bytes", "name": "path", "type": "bytes"},
                        {
                            "internalType": "address",
                            "name": "recipient",
                            "type": "address",
                        },
                        {
                            "internalType": "uint256",
                            "name": "deadline",
                            "type": "uint256",
                        },
                        {
                            "internalType": "uint256",
                            "name": "amountOut",
                            "type": "uint256",
                        },
                        {
                            "internalType": "uint256",
                            "name": "amountInMaximum",
                            "type": "uint256",
                        },
                    ],
                    "internalType": "struct ISwapRouter.ExactOutputParams",
                    "name": "params",
                    "type": "tuple",
                }
            ],
            "name": "exactOutput",
            "outputs": [
                {"internalType": "uint256", "name": "amountIn", "type": "uint256"}
            ],
            "stateMutability": "payable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "components": [
                        {
                            "internalType": "address",
                            "name": "tokenIn",
                            "type": "address",
                        },
                        {
                            "internalType": "address",
                            "name": "tokenOut",
                            "type": "address",
                        },
                        {"internalType": "uint24", "name": "fee", "type": "uint24"},
                        {
                            "internalType": "address",
                            "name": "recipient",
                            "type": "address",
                        },
                        {
                            "internalType": "uint256",
                            "name": "deadline",
                            "type": "uint256",
                        },
                        {
                            "internalType": "uint256",
                            "name": "amountOut",
                            "type": "uint256",
                        },
                        {
                            "internalType": "uint256",
                            "name": "amountInMaximum",
                            "type": "uint256",
                        },
                        {
                            "internalType": "uint160",
                            "name": "sqrtPriceLimitX96",
                            "type": "uint160",
                        },
                    ],
                    "internalType": "struct ISwapRouter.ExactOutputSingleParams",
                    "name": "params",
                    "type": "tuple",
                }
            ],
            "name": "exactOutputSingle",
            "outputs": [
                {"internalType": "uint256", "name": "amountIn", "type": "uint256"}
            ],
            "stateMutability": "payable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "factory",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "bytes[]", "name": "data", "type": "bytes[]"}],
            "name": "multicall",
            "outputs": [
                {"internalType": "bytes[]", "name": "results", "type": "bytes[]"}
            ],
            "stateMutability": "payable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "refundETH",
            "outputs": [],
            "stateMutability": "payable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "token", "type": "address"},
                {"internalType": "uint256", "name": "value", "type": "uint256"},
                {"internalType": "uint256", "name": "deadline", "type": "uint256"},
                {"internalType": "uint8", "name": "v", "type": "uint8"},
                {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                {"internalType": "bytes32", "name": "s", "type": "bytes32"},
            ],
            "name": "selfPermit",
            "outputs": [],
            "stateMutability": "payable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "token", "type": "address"},
                {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                {"internalType": "uint256", "name": "expiry", "type": "uint256"},
                {"internalType": "uint8", "name": "v", "type": "uint8"},
                {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                {"internalType": "bytes32", "name": "s", "type": "bytes32"},
            ],
            "name": "selfPermitAllowed",
            "outputs": [],
            "stateMutability": "payable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "token", "type": "address"},
                {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                {"internalType": "uint256", "name": "expiry", "type": "uint256"},
                {"internalType": "uint8", "name": "v", "type": "uint8"},
                {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                {"internalType": "bytes32", "name": "s", "type": "bytes32"},
            ],
            "name": "selfPermitAllowedIfNecessary",
            "outputs": [],
            "stateMutability": "payable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "token", "type": "address"},
                {"internalType": "uint256", "name": "value", "type": "uint256"},
                {"internalType": "uint256", "name": "deadline", "type": "uint256"},
                {"internalType": "uint8", "name": "v", "type": "uint8"},
                {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                {"internalType": "bytes32", "name": "s", "type": "bytes32"},
            ],
            "name": "selfPermitIfNecessary",
            "outputs": [],
            "stateMutability": "payable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "token", "type": "address"},
                {"internalType": "uint256", "name": "amountMinimum", "type": "uint256"},
                {"internalType": "address", "name": "recipient", "type": "address"},
            ],
            "name": "sweepToken",
            "outputs": [],
            "stateMutability": "payable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "token", "type": "address"},
                {"internalType": "uint256", "name": "amountMinimum", "type": "uint256"},
                {"internalType": "address", "name": "recipient", "type": "address"},
                {"internalType": "uint256", "name": "feeBips", "type": "uint256"},
                {"internalType": "address", "name": "feeRecipient", "type": "address"},
            ],
            "name": "sweepTokenWithFee",
            "outputs": [],
            "stateMutability": "payable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "int256", "name": "amount0Delta", "type": "int256"},
                {"internalType": "int256", "name": "amount1Delta", "type": "int256"},
                {"internalType": "bytes", "name": "_data", "type": "bytes"},
            ],
            "name": "uniswapV3SwapCallback",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "uint256", "name": "amountMinimum", "type": "uint256"},
                {"internalType": "address", "name": "recipient", "type": "address"},
            ],
            "name": "unwrapWETH9",
            "outputs": [],
            "stateMutability": "payable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "uint256", "name": "amountMinimum", "type": "uint256"},
                {"internalType": "address", "name": "recipient", "type": "address"},
                {"internalType": "uint256", "name": "feeBips", "type": "uint256"},
                {"internalType": "address", "name": "feeRecipient", "type": "address"},
            ],
            "name": "unwrapWETH9WithFee",
            "outputs": [],
            "stateMutability": "payable",
            "type": "function",
        },
        {"stateMutability": "payable", "type": "receive"},
    ],
    "quoter": [
        {
            "inputs": [
                {"internalType": "address", "name": "_factory", "type": "address"},
                {"internalType": "address", "name": "_WETH9", "type": "address"},
            ],
            "stateMutability": "nonpayable",
            "type": "constructor",
        },
        {
            "inputs": [],
            "name": "WETH9",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "factory",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes", "name": "path", "type": "bytes"},
                {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
            ],
            "name": "quoteExactInput",
            "outputs": [
                {"internalType": "uint256", "name": "amountOut", "type": "uint256"},
                {
                    "internalType": "uint160[]",
                    "name": "sqrtPriceX96AfterList",
                    "type": "uint160[]",
                },
                {
                    "internalType": "uint32[]",
                    "name": "initializedTicksCrossedList",
                    "type": "uint32[]",
                },
                {"internalType": "uint256", "name": "gasEstimate", "type": "uint256"},
            ],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "components": [
                        {
                            "internalType": "address",
                            "name": "tokenIn",
                            "type": "address",
                        },
                        {
                            "internalType": "address",
                            "name": "tokenOut",
                            "type": "address",
                        },
                        {
                            "internalType": "uint256",
                            "name": "amountIn",
                            "type": "uint256",
                        },
                        {"internalType": "uint24", "name": "fee", "type": "uint24"},
                        {
                            "internalType": "uint160",
                            "name": "sqrtPriceLimitX96",
                            "type": "uint160",
                        },
                    ],
                    "internalType": "struct IQuoterV2.QuoteExactInputSingleParams",
                    "name": "params",
                    "type": "tuple",
                }
            ],
            "name": "quoteExactInputSingle",
            "outputs": [
                {"internalType": "uint256", "name": "amountOut", "type": "uint256"},
                {
                    "internalType": "uint160",
                    "name": "sqrtPriceX96After",
                    "type": "uint160",
                },
                {
                    "internalType": "uint32",
                    "name": "initializedTicksCrossed",
                    "type": "uint32",
                },
                {"internalType": "uint256", "name": "gasEstimate", "type": "uint256"},
            ],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes", "name": "path", "type": "bytes"},
                {"internalType": "uint256", "name": "amountOut", "type": "uint256"},
            ],
            "name": "quoteExactOutput",
            "outputs": [
                {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
                {
                    "internalType": "uint160[]",
                    "name": "sqrtPriceX96AfterList",
                    "type": "uint160[]",
                },
                {
                    "internalType": "uint32[]",
                    "name": "initializedTicksCrossedList",
                    "type": "uint32[]",
                },
                {"internalType": "uint256", "name": "gasEstimate", "type": "uint256"},
            ],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "components": [
                        {
                            "internalType": "address",
                            "name": "tokenIn",
                            "type": "address",
                        },
                        {
                            "internalType": "address",
                            "name": "tokenOut",
                            "type": "address",
                        },
                        {
                            "internalType": "uint256",
                            "name": "amount",
                            "type": "uint256",
                        },
                        {"internalType": "uint24", "name": "fee", "type": "uint24"},
                        {
                            "internalType": "uint160",
                            "name": "sqrtPriceLimitX96",
                            "type": "uint160",
                        },
                    ],
                    "internalType": "struct IQuoterV2.QuoteExactOutputSingleParams",
                    "name": "params",
                    "type": "tuple",
                }
            ],
            "name": "quoteExactOutputSingle",
            "outputs": [
                {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
                {
                    "internalType": "uint160",
                    "name": "sqrtPriceX96After",
                    "type": "uint160",
                },
                {
                    "internalType": "uint32",
                    "name": "initializedTicksCrossed",
                    "type": "uint32",
                },
                {"internalType": "uint256", "name": "gasEstimate", "type": "uint256"},
            ],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "int256", "name": "amount0Delta", "type": "int256"},
                {"internalType": "int256", "name": "amount1Delta", "type": "int256"},
                {"internalType": "bytes", "name": "path", "type": "bytes"},
            ],
            "name": "uniswapV3SwapCallback",
            "outputs": [],
            "stateMutability": "view",
            "type": "function",
        },
    ],
}


TOKENS_PER_CHAIN = {
    "Ethereum": {
        "ETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    },
    "Arbitrum": {
        "ETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        "WETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        "ARB": "0x912CE59144191C1204E64559FE8253a0e49E6548",
        "USDC": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
        "USDT": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
        "USDC.e": "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8",
        "DAI": "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
    },
    "Zora": {
        "ETH": "0x4200000000000000000000000000000000000006",
        "WETH": "0x4200000000000000000000000000000000000006",
    },
    "Optimism": {
        "ETH": "0x4200000000000000000000000000000000000006",
        "WETH": "0x4200000000000000000000000000000000000006",
        "OP": "0x4200000000000000000000000000000000000042",
        "USDC": "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85",
        "USDT": "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58",
        "USDC.e": "0x7F5c764cBc14f9669B88837ca1490cCa17c31607",
        "DAI": "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
    },
    "Base": {
        "ETH": "0x4200000000000000000000000000000000000006",
        "WETH": "0x4200000000000000000000000000000000000006",
        "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "USDC.e": "0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA",
    },
    "Linea": {
        "ETH": "0xe5D7C2a44FfDDf6b295A15c148167daaAf5Cf34f",
        "WETH": "0xe5D7C2a44FfDDf6b295A15c148167daaAf5Cf34f",
        "USDT": "0xA219439258ca9da29E9Cc4cE5596924745e12B93",
        "USDC": "0x176211869cA2b568f2A7D4EE941E073a821EE1ff",
    },
    "Scroll": {
        "ETH": "0x5300000000000000000000000000000000000004",
        "WETH": "0x5300000000000000000000000000000000000004",
        "USDT": "0xf55BEC9cafDbE8730f096Aa55dad6D22d44099Df",
        "USDC": "0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4",
    },
}
