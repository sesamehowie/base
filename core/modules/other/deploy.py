import random
from typing import Self
from eth_account import Account
from core.utils.w3_manager import EthManager
from web3 import Web3
from eth_typing import HexStr
from loguru import logger
from core.utils.networks import Network
from core.utils.custom_wrappers import exception_handler_with_retry
from config import STORAGE_ABI, OWNER_ABI, VOTER_ABI


class Deploy:
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
        self.module_name = "Contract Deployment"

        self.logger.debug(f"Now working: module {self.module_name}")

        self.contract_bytecode_mapping = {
            "OmniBTC": {
                "data": "0x608060405243600055348015601357600080fd5b5060358060216000396000f3fe6080604052600080fdfea165627a7a72305820ba621ecf7b70183d2bc65f3b3a1ab23211f1ccdf5d5b61213d5ecd3f20ffefa60029",
                "abi": [],
            },
            "Owlto": {
                "data": "0x6080604052348015600f57600080fd5b50603f80601d6000396000f3fe6080604052600080fdfea2646970667358221220bc612630cc0a226fd67c37cd542e43e860635ca379bfc2fd320a9af6eed16c6664736f6c63430008120033",
                "abi": [],
            },
            "Merkly": {
                "data": "0x60806040526000805461ffff1916905534801561001b57600080fd5b5060fb8061002a6000396000f3fe6080604052348015600f57600080fd5b506004361060325760003560e01c80630c55699c146037578063b49004e914605b575b600080fd5b60005460449061ffff1681565b60405161ffff909116815260200160405180910390f35b60616063565b005b60008054600191908190607a90849061ffff166096565b92506101000a81548161ffff021916908361ffff160217905550565b61ffff81811683821601908082111560be57634e487b7160e01b600052601160045260246000fd5b509291505056fea2646970667358221220666c87ec501268817295a4ca1fc6e3859faf241f38dd688f145135970920009264736f6c63430008120033",
                "abi": [],
            },
            "Owner": {
                "data": "0x6080604052348015600e575f80fd5b50335f806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055505f8054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff165f73ffffffffffffffffffffffffffffffffffffffff167f342827c97908e5e2f71151c08502a66d44b6f758e3ac2f1de95f02eb95f0a73560405160405180910390a3610340806100d45f395ff3fe608060405234801561000f575f80fd5b5060043610610034575f3560e01c8063893d20e814610038578063a6f9dae114610056575b5f80fd5b610040610072565b60405161004d9190610220565b60405180910390f35b610070600480360381019061006b9190610267565b610099565b005b5f805f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff16905090565b5f8054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614610126576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161011d906102ec565b60405180910390fd5b8073ffffffffffffffffffffffffffffffffffffffff165f8054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff167f342827c97908e5e2f71151c08502a66d44b6f758e3ac2f1de95f02eb95f0a73560405160405180910390a3805f806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050565b5f73ffffffffffffffffffffffffffffffffffffffff82169050919050565b5f61020a826101e1565b9050919050565b61021a81610200565b82525050565b5f6020820190506102335f830184610211565b92915050565b5f80fd5b61024681610200565b8114610250575f80fd5b50565b5f813590506102618161023d565b92915050565b5f6020828403121561027c5761027b610239565b5b5f61028984828501610253565b91505092915050565b5f82825260208201905092915050565b7f43616c6c6572206973206e6f74206f776e6572000000000000000000000000005f82015250565b5f6102d6601383610292565b91506102e1826102a2565b602082019050919050565b5f6020820190508181035f830152610303816102ca565b905091905056fea26469706673582212201e18133d143e7371ebe6c6f4e86cb76c857c326cedd33e6240504260f0d34eeb64736f6c634300081a0033",
                "abi": OWNER_ABI,
            },
            "Voter": {
                "data": "0x6080604052348015600e575f80fd5b50335f806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055505f8054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff165f73ffffffffffffffffffffffffffffffffffffffff167f342827c97908e5e2f71151c08502a66d44b6f758e3ac2f1de95f02eb95f0a73560405160405180910390a3610340806100d45f395ff3fe608060405234801561000f575f80fd5b5060043610610034575f3560e01c8063893d20e814610038578063a6f9dae114610056575b5f80fd5b610040610072565b60405161004d9190610220565b60405180910390f35b610070600480360381019061006b9190610267565b610099565b005b5f805f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff16905090565b5f8054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614610126576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161011d906102ec565b60405180910390fd5b8073ffffffffffffffffffffffffffffffffffffffff165f8054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff167f342827c97908e5e2f71151c08502a66d44b6f758e3ac2f1de95f02eb95f0a73560405160405180910390a3805f806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050565b5f73ffffffffffffffffffffffffffffffffffffffff82169050919050565b5f61020a826101e1565b9050919050565b61021a81610200565b82525050565b5f6020820190506102335f830184610211565b92915050565b5f80fd5b61024681610200565b8114610250575f80fd5b50565b5f813590506102618161023d565b92915050565b5f6020828403121561027c5761027b610239565b5b5f61028984828501610253565b91505092915050565b5f82825260208201905092915050565b7f43616c6c6572206973206e6f74206f776e6572000000000000000000000000005f82015250565b5f6102d6601383610292565b91506102e1826102a2565b602082019050919050565b5f6020820190508181035f830152610303816102ca565b905091905056fea26469706673582212201e18133d143e7371ebe6c6f4e86cb76c857c326cedd33e6240504260f0d34eeb64736f6c634300081a0033",
                "abi": VOTER_ABI,
            },
            "Storage": {
                "data": "0x6080604052348015600e575f80fd5b506101438061001c5f395ff3fe608060405234801561000f575f80fd5b5060043610610034575f3560e01c80632e64cec1146100385780636057361d14610056575b5f80fd5b610040610072565b60405161004d919061009b565b60405180910390f35b610070600480360381019061006b91906100e2565b61007a565b005b5f8054905090565b805f8190555050565b5f819050919050565b61009581610083565b82525050565b5f6020820190506100ae5f83018461008c565b92915050565b5f80fd5b6100c181610083565b81146100cb575f80fd5b50565b5f813590506100dc816100b8565b92915050565b5f602082840312156100f7576100f66100b4565b5b5f610104848285016100ce565b9150509291505056fea26469706673582212209a0dd35336aff1eb3eeb11db76aa60a1427a12c1b92f945ea8c8d1dfa337cf2264736f6c634300081a0033",
                "abi": STORAGE_ABI,
            },
            "BasicMath": {
                "data": "0x6080604052348015600e575f5ffd5b506102b18061001c5f395ff3fe608060405234801561000f575f5ffd5b5060043610610034575f3560e01c806306b034e9146100385780635270312a14610069575b5f5ffd5b610052600480360381019061004d919061015a565b61009a565b6040516100609291906101c1565b60405180910390f35b610083600480360381019061007e919061015a565b6100f4565b6040516100919291906101c1565b60405180910390f35b5f5f837fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff6100c89190610215565b8311156100db575f6001915091506100ed565b82846100e79190610248565b5f915091505b9250929050565b5f5f8383111561010a575f60019150915061011c565b82846101169190610215565b5f915091505b9250929050565b5f5ffd5b5f819050919050565b61013981610127565b8114610143575f5ffd5b50565b5f8135905061015481610130565b92915050565b5f5f604083850312156101705761016f610123565b5b5f61017d85828601610146565b925050602061018e85828601610146565b9150509250929050565b6101a181610127565b82525050565b5f8115159050919050565b6101bb816101a7565b82525050565b5f6040820190506101d45f830185610198565b6101e160208301846101b2565b9392505050565b7f4e487b71000000000000000000000000000000000000000000000000000000005f52601160045260245ffd5b5f61021f82610127565b915061022a83610127565b9250828203905081811115610242576102416101e8565b5b92915050565b5f61025282610127565b915061025d83610127565b9250828201905080821115610275576102746101e8565b5b9291505056fea26469706673582212205a351da00d9c0a8163a69679be28933d54b6da26aa6e67e4fa6ae0e9542d358564736f6c634300081c0033",
                "abi": [],
            },
        }

    def get_random_contract(self) -> dict[str, str]:

        return self.contract_bytecode_mapping[
            random.choice(list(self.contract_bytecode_mapping.keys()))
        ]

    @exception_handler_with_retry
    def create_contract(self, creation_data: dict[str, str]) -> bool:
        self.logger.info(
            f"{self.account_name} | {self.address} | {self.module_name} | Deploying contract..."
        )

        self.client.w3.eth.default_account = self.address

        contract = self.client.w3.eth.contract(
            abi=creation_data["abi"], bytecode=creation_data["data"][2:]
        )

        tx_params = contract.constructor().build_transaction(
            {
                "from": self.address,
                "nonce": self.client.w3.eth.get_transaction_count(self.address),
                "chainId": self.network.chain_id,
            }
        )

        tx_params["gas"] = 300000

        signed = self.client.sign_transaction(tx_dict=tx_params)

        if signed:
            tx_hash = self.client.send_tx(signed_tx=signed)

            if tx_hash:
                return True

            return False

        return

    def run_deploy(self) -> bool:
        rand_data = self.get_random_contract()

        res = self.create_contract(creation_data=rand_data)

        return True if res else False
