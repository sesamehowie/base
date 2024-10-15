from eth_typing import HexStr
from dataclasses import dataclass
from typing import Any
from config import STIX_ABI, CLAIMABLE_ABI, MIGGLES_ABI, BASE_NFT_ABI


class MintType:
    def __init__(self, type_id: int, function_name: str):
        self.type_id = type_id
        self.function_name = function_name

    def get_interface(self, wallet_address: str, mint_price: int) -> list:
        interface_mapping = {
            1: [wallet_address, 1, ""],
            2: f"0x84bb1e42000000000000000000000000{wallet_address.lower()[2:]}0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c00000000000000000000000000000000000000000000000000000000000000180000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001d4da48b00000000",
            3: f"0x57bc3d78000000000000000000000000{wallet_address.lower()[2:]}00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e000000000000000000000000000000000000000000000000000000000000001a0000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000640000000000000000000000000000000000000000000000000000000000000000000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
        }

        return interface_mapping[self.type_id]


class MintTypes:
    Default = MintType(type_id=1, function_name="mintWithComment")
    Claim = MintType(type_id=2, function_name="claim")
    ClaimWithId = MintType(type_id=3, function_name="claim")


class Mint:

    def __init__(
        self,
        name: str,
        mint_address: str | HexStr,
        challenge_id: str,
        abi: Any = BASE_NFT_ABI,
        default_gas: int = 200000,
        type: MintType = MintTypes.Default,
        mint_price: int = 0,
        is_active: bool = True,
    ):
        self.name = name
        self.mint_address = mint_address
        self.default_gas = default_gas
        self.challenge_id = challenge_id
        self.abi = abi
        self.type = type
        self.mint_price = mint_price
        self.is_active = is_active

    def get_point_data(self, wallet_address: str) -> dict:
        return {
            "challengeId": self.challenge_id,
            "gameId": 2,
            "userAddress": wallet_address,
        }


@dataclass
class Mints:
    BaseIsForEveryone = Mint(
        name="Base is for everyone",
        mint_address="0xFcdb05f3ee36B03be6c2e8D9caF112227039e7F7",
        challenge_id="7MmQcBU7kU54g4hBiM9dFj",
        mint_price=100000000000000,
    )
    Billboard = Mint(
        name="Billboard",
        mint_address="0xf9aDb505EaadacCF170e48eE46Ee4d5623f777d7",
        challenge_id="4XFHKaEgswlQCR4fDJnIZH",
        mint_price=800000000000000,
        is_active=False,
    )
    BreakingThrough = Mint(
        name="Breaking Through",
        mint_address="0x96E82d88c07eCa6a29B2AD86623397B689380652",
        challenge_id="78AUXYw8UCyFUPE2zy9yMZ",
        mint_price=100000000000000,
    )
    EthCantBeStopped = Mint(
        name="ETH can't be stopped",
        mint_address="0xb0FF351AD7b538452306d74fB7767EC019Fa10CF",
        challenge_id="ocsChallenge_c1de2373-35ad-4f3c-ab18-4dfadf15754d",
        mint_price=100000000000000,
    )
    Chibling = Mint(
        name="Chibling",
        mint_address="0x13F294BF5e26843C33d0ae739eDb8d6B178740B0",
        challenge_id="5Ip1kHz9vEZDTazTiBWbKh",
        mint_price=100000000000000,
        is_active=False,
    )
    EtfCelebration = Mint(
        name="ETF Celebration",
        mint_address="0xb5408b7126142C61f509046868B1273F96191b6d",
        challenge_id="5e383RWcRtGAwGUorkGiYC",
        mint_price=100000000000000,
        default_gas=190000,
    )
    Etfereum = Mint(
        name="ETFEREUM",
        mint_address="0xb5408b7126142C61f509046868B1273F96191b6d",
        challenge_id="ocsChallenge_eba9e6f0-b7b6-4d18-8b99-a64aea045117",
        mint_price=100000000000000,
        default_gas=190000,
    )
    EurcLiveOnBase = Mint(
        name="EURC is live on Base",
        mint_address="0x615194d9695d0c02Fc30a897F8dA92E17403D61B",
        challenge_id="1iZiHPbqaIGW5F08bCit6J",
        mint_price=100000000000000,
    )
    HappyBirthdayToshi = Mint(
        name="Happy Birthday Toshi",
        mint_address="0xE65dFa5C8B531544b5Ae4960AE0345456D87A47D",
        challenge_id="1pjoNf5onjgsi7r9fWp3ob",
        mint_price=100000000000000,
    )
    MisterMiggles = Mint(
        name="Mister Miggles",
        mint_address="0xDc03a75F96f38615B3eB55F0F289d36E7A706660",
        challenge_id="ocsChallenge_d0778cee-ad0b-46b9-93d9-887b917b2a1f",
        abi=MIGGLES_ABI,
        type=MintTypes.ClaimWithId,
        mint_price=100000000000000,
    )
    BuildOnboardAndGrow = Mint(
        name="Build, Onboard and Grow",
        mint_address="0x0b9fa0Ca5B64c05f9C3Ca3D580e84883f1867d76",
        challenge_id="nBEpkjoXgD2BbdfSMxeQz",
        mint_price=100000000000000,
    )
    TeamLiquid = Mint(
        name="Team Liquid",
        mint_address="0x1b9ac8580d2e81d7322f163362831448e7fcad1b",
        challenge_id="6VRBNN6qr2algysZeorek8",
        abi=CLAIMABLE_ABI,
        type=MintTypes.Claim,
        mint_price=0,
    )
    WelcomeOnchain = Mint(
        name="Welcome Onchain",
        mint_address="0x6B033e8199ce2E924813568B716378aA440F4C67",
        challenge_id="78zcHkWSABcPWMoacVI9Vs",
        type=MintTypes.Claim,
        mint_price=100000000000000,
        abi=CLAIMABLE_ABI,
        is_active=False,
    )
    WorldAfterEtf = Mint(
        name="World After ETF",
        mint_address="0x955FdFdFd783C89Beb54c85f0a97F0904D85B86C",
        challenge_id="ocsChallenge_65c17605-e085-4528-b4f1-76ce5f48da56",
        mint_price=100000000000000,
        default_gas=190000,
    )
    SuperBasedBuilders = Mint(
        name="Super Based Builders",
        mint_address="0xc611fd3554a1ebf0e5eeD6F597DAaa50dA90FB08",
        challenge_id="ocsChallenge_96f49d53-ccf0-4863-bafa-37a345096dd6",
        mint_price=100000000000000,
        default_gas=150000,
    )
    SpeedTracker = Mint(
        name="SpeedTracker",
        mint_address="0xCD45E55DB12E9CA3E82370F5D0c5C6876bF6f466",
        challenge_id="4eZGLIjK9SRmXeAxicTY5H",
        mint_price=100000000000000,
    )
    SeasonalErosion = Mint(
        name="Seasonal Erosion",
        mint_address="0x2aa80a13395425EF3897c9684a0249a5226eA779",
        challenge_id="6mpsE4jgRI0GnuU3elo2XV",
        mint_price=100000000000000,
        is_active=False,
    )
    PixotchiSeed = Mint(
        name="Pixotchi Seed",
        mint_address="0xeb4e16c804AE9275a655AbBc20cD0658A91F9235",
        challenge_id="ocsChallenge_42603619-8299-4142-a9e2-5100c8bf1a89",
        mint_price=100000000000000,
    )
    CityVerse = Mint(
        name="CityVerse",
        mint_address="0x2E2c0753fc81BE22381c674ADD7A05F24cfD9761",
        challenge_id="ocsChallenge_14c35bdd-3a9f-4b31-af73-d7438696e91c",
        mint_price=100000000000000,
    )
    Summer24 = Mint(
        name="Summer 24",
        mint_address="0x9D2FC5fFE5939Efd1d573f975BC5EEFd364779ae",
        challenge_id="ocsChallenge_1287a985-e4b1-4f30-b508-306c4d109832",
        mint_price=100000000000000,
    )
    TheThirdNouniversary = Mint(
        name="The 3rd Nouniversary",
        mint_address="0xae954896B4d3B113C9FCe85f64387229291fb5a9",
        challenge_id="7ktuPuO5kUtvQmvzd4T5r3",
        mint_price=100000000000000,
    )
    CelebratingNouns = Mint(
        name="Celebrating Nouns",
        mint_address="0x5680eAD37A60604a12F821Bb9Da42858cbC346Fd",
        challenge_id="6VA9MQosJnPcCwEeNkNVsW",
        mint_price=100000000000000,
    )
    BasedNouns = Mint(
        name="Based Nouns",
        mint_address="0x6414A4359848d2BF12B93483cd8A6ef6B03779ae",
        challenge_id="71QheN8IVzfyoVtE8oeHNU",
        mint_price=100000000000000,
    )
    NounsForever = Mint(
        name="Nouns Forever",
        mint_address="0xcF74F48B71f2A8160aDa67D1720ce0F2778b5a28",
        challenge_id="3M9bT5pBKJE6jgolwMFsJU",
        mint_price=100000000000000,
    )
    NounsEverywhere = Mint(
        name="Nouns Everywhere",
        mint_address="0x63197bb4dE33DA81FdB311Ef6395237fB0F65C7D",
        challenge_id="ocsChallenge_d122a59b-6a04-4949-9cdb-b9262e843aa6",
        mint_price=100000000000000,
    )
    HappyNouniversary = Mint(
        name="Happy Nouniversary",
        mint_address="0xE0fE6DD851187c62a79D00a211953Fe3B5Cec7FE",
        challenge_id="44wp1P8LSnwkPSz7Ft3q78",
        mint_price=100000000000000,
    )
    EndOfNounsSzn = Mint(
        name="End of Nouns Szn. 3",
        mint_address="0x7B28d9Efa325225666Aa6ddaC20c46420cd75871",
        challenge_id="ocsChallenge_15259510-7040-4f16-bdfa-f137846b546c",
        mint_price=100000000000000,
    )
    NounishVibes = Mint(
        name="Nounish Vibes",
        mint_address="0xCcbb9DC3FeCAf7a9cAe716eF1C16C8ca2f19a3D1",
        challenge_id="2r8tpvuVPkYIuhAWSoMYY1",
        mint_price=100000000000000,
    )
    HandOfNouns = Mint(
        name="Hand of Nouns",
        mint_address="0x250d4678a1175113eC96e7DeB90584267026D443",
        challenge_id="2qOcpUCs12XwgLUpoQQgYT",
        mint_price=100000000000000,
    )
    MiggsWifNouns = Mint(
        name="Miggs wif Nouns",
        mint_address="0x25F98e990B6C0dBa5A109B92542F16DCbbD017C8",
        challenge_id="1eeRIVPiOVBJ3rlM5sGnpx",
        mint_price=100000000000000,
    )
    NounifyTheRockies = Mint(
        name="Nounify The Rockies",
        mint_address="0x306671092213C4d0da1a7bB5c31D5B4F9aB62246",
        challenge_id="21pui4pvJ0h6YA8EAlvjqh",
        mint_price=100000000000000,
    )
    CoffeeDays = Mint(
        name="Coffee Days 2024",
        mint_address="0xf16755b43eE1a458161f0faE5a9124729f4f6B1B",
        challenge_id="ocsChallenge_9142cba1-ec12-4ee8-915e-7976536908cd",
        default_gas=350000,
        mint_price=600000000000000,
    )
    NounsSummerCelebration = Mint(
        name="Nouns Summer Celebration",
        mint_address="0x01F0D0D40D4BB499e7CB35940E908b74D08BA412",
        challenge_id="TqnsSrVTggFzdu9vFuSju",
        mint_price=100000000000000,
    )
    NounMoon = Mint(
        name="Noun Moon",
        mint_address="0x92440f15451f1058237a83B2fD64C67110C5146B",
        challenge_id="ocsChallenge_d9e15d6a-3c6e-4585-91ff-ba9e157f3789",
        mint_price=100000000000000,
    )
    WalkingOnSunshine = Mint(
        name="Walking on Sunshine",
        mint_address="0x4E4c12451A6e2473Fc4C63f84E175C3D31555F47",
        challenge_id="22B38pVH5SN5yAiW6HYdNa",
        mint_price=100000000000000,
    )
    Consolation = Mint(
        name="Consolation of Chroma Convergence",
        mint_address="0x7d22F7EC034bB1060E033f132b0b23aA45b2B9B4",
        challenge_id="6FfxTruNSVDFLtvD3hb9sT",
        mint_price=100000000000000,
    )
    HappyBornThirdDay = Mint(
        name="Happy born 3rd day",
        mint_address="0x037A8002604cB2C1871204Ca868536B7D696df1d",
        challenge_id="2U6YRYo55Zgfcxull5C1Xn",
        mint_price=100000000000000,
    )
    BaseTurnsOne = Mint(
        name="Base Turns One",
        mint_address="0x96C7464c73c24e3cBF3CcA8f3a2BFF917F39dC26",
        challenge_id="ocsChallenge_3809bf6d-a2d1-4e15-84e7-74beac310661",
        mint_price=400000000000000,
        default_gas=190000,
    )
    DawnOfDaylight = Mint(
        name="Dawn Of Daylight",
        mint_address="0x31B81650997e26Eb527CA6541B1433d1EF348d93",
        challenge_id="ocsChallenge_18c8180f-2818-41b7-bc10-6dbd53d86260",
        abi=CLAIMABLE_ABI,
        type=MintTypes.Claim,
        mint_price=0,
    )
    StixTournamentPass = Mint(
        name="STIX Tournament Pass",
        mint_address="0xa7891c87933BB99Db006b60D8Cb7cf68141B492f",
        challenge_id="ocsChallenge_bd5208b5-ff1e-4f5b-8522-c4d4ebb795b7",
        abi=STIX_ABI,
        type=MintTypes.Claim,
        mint_price=0,
    )
    Strut001 = Mint(
        name="strut 001",
        mint_address="0x9FF8Fd82c0ce09caE76e777f47d536579AF2Fe7C",
        challenge_id="5c3PqZ2EGVbzQ2CQXL1vWK",
        mint_price=100000000000000,
    )
    Butterfly = Mint(
        name="Butterfly",
        mint_address="0x3b4B32a5c9A01763A0945A8a4a4269052DC3DE2F",
        challenge_id="6UuHdstl9MRFd4cgFf15kk",
        mint_price=100000000000000,
    )
    ToshiChess = Mint(
        name="Toshi Chess",
        mint_address="0xd60f13cC3e4d5bC96e7bAE8AAb5F448f3eFF3F0C",
        challenge_id="1HMONONDaMukjieAOD3PHQ",
        mint_price=100000000000000,
    )
    BaseCanada = Mint(
        name="Base Canada",
        mint_address="0x7B791EdF061Df65bAC7a9d47668F61F1a9A998C0",
        challenge_id="1BWyKWI2UZHnOEw8E4hpS5",
        default_gas=190000,
        mint_price=100000000000000,
    )
    WatchuLookingAt = Mint(
        name="Watchu Looking at?",
        mint_address="0x5307c5ee9AeE0B944fA2E0Dba5D35D1D454E4bcE",
        challenge_id="39XYCR1jsdPwnoFEpwCwhD",
        default_gas=190000,
        mint_price=111000000000000,
    )
    SummerSerenity = Mint(
        name="Summer Serenity",
        mint_address="0x310d51391955b6ffd7d8afbb5981dcfe0f87ce6a",
        challenge_id="ocsChallenge_e490f19f-1923-479d-83b8-25ecdc3b8c4a",
        mint_price=111000000000000,
        default_gas=190000,
    )
    Memloop = Mint(
        name="Memloop",
        mint_address="0xc1cab3aef83578ea237ba98e5562e698c2a08247",
        challenge_id="ocsChallenge_a40fe1f2-c33f-4ead-aeba-edfbe1ef33b0",
        mint_price=111000000000000,
        default_gas=190000,
    )
    ThinkBig = Mint(
        name="Think Big",
        mint_address="0x752d593b3B8aD1c5d827F5B9AA9b653eE7134ea0",
        challenge_id="3EOQYszODyvZvbQMoKPoDO",
        mint_price=100000000000000,
        default_gas=190000,
    )
    ToshiVibe = Mint(
        name="Toshi Vibe",
        mint_address="0xbFa3fF9dcdB811037Bbec89f89E2751114ECD299",
        challenge_id="3WE9nylUC2bMHz9c6hxFnL",
        mint_price=100000000000000,
        default_gas=190000,
    )
    NounsUnderCover = Mint(
        name="Nouns Undercover",
        mint_address="0xa587c8a61418d3099e1f167c631ce37891474c67",
        challenge_id="ocsChallenge_7f809561-5fc7-4edb-8696-0937f70a8741",
        mint_price=111000000000000,
        default_gas=190000,
    )
    BaseEns = Mint(
        name="Base Domain Name",
        mint_address="0x1c4ABb26936c050A864E23017881e588DDB4E9F4",
        challenge_id="2XaiAPDQ8WwG5CUWfMMYaU",
        mint_price=0,
        default_gas=611000,
    )
    DualityInMotion = Mint(
        name="Duality in Motion",
        mint_address="0x5b45498D20d24D9c6Da165eDcd0eBcE0636176Ae",
        challenge_id="3Po39fHlC66muE3X5IHNfs",
        mint_price=100000000000000,
        default_gas=190000,
    )
    StandWithCrypto = Mint(
        name="Stand With Crypto",
        mint_address="0x146B627a763DFaE78f6A409CEF5B8ad84dDD4150",
        challenge_id="3ofLIMuInVt5sKkQOtLWp0",
        mint_price=100000000000000,
        default_gas=190000,
    )
    StandWithCryptoPizza = Mint(
        name="Stand With Crypto Pizza",
        mint_address="0x4beAdC00E2A6b6C4fAc1a43FF340E5D71CBB9F77",
        challenge_id="1zbecUKJMKwyYoKOn2OV5n",
        mint_price=100000000000000,
        default_gas=190000,
    )
    StandWithCryptoShield = Mint(
        name="What if we added a Stand With Crypto shield?",
        mint_address="0xea50e58B518435AD2CeCE84d1e099b2e0878B9cF",
        challenge_id="71fCEn2cIwqXqLE6wYxGl0",
        mint_price=100000000000000,
        default_gas=190000,
    )
    CryptoWillBloom = Mint(
        name="Crypto will bloom",
        mint_address="0x651b0A2b9FB9C186fB6C9a9CEddf25B791Ad5753",
        challenge_id="S3DyUSaz6mYehsypyOqPD",
        mint_price=100000000000000,
        default_gas=190000,
    )
    StandWithCryptoSong = Mint(
        name="Stand With Crypto Folk Song",
        mint_address="0x2382456097cC12ce54052084e9357612497FD6be",
        challenge_id="5Hyw2HMBfOBFDvCBkvdVmX",
        mint_price=100000000000000,
        default_gas=190000,
    )
    JuicyAdventure = Mint(
        name="Juicy Adventure",
        mint_address="0x6ba5Ba71810c1196f20123B57B66C9ed2A5dBd76",
        challenge_id="ocsChallenge_3b1c2886-3168-45c7-b2cd-b590cde66c61",
        mint_price=0,
        default_gas=590000,
    )
    EspressoAndMilk = Mint(
        name="Espresso and milk",
        mint_address="0x52088a4416a9D437fC4a20a147103B4450e1bfd2",
        challenge_id="ocsChallenge_668763d8-477c-444b-91e1-346a69a8146d",
        mint_price=500000000000000,
        default_gas=190000,
    )
    PalomarGroup = Mint(
        name="Palomar Group",
        mint_address="0xbcbed193fbc6bba740607e64cc26042d052ebe85",
        challenge_id="ocsChallenge_1c4878b7-f846-44cd-a2fe-5c91b1e27cd6",
        mint_price=777000000000000,
        default_gas=230000,
    )
    StandWithCryptoRune = Mint(
        name="Stand With Crypto Shield Rune",
        mint_address="0x13fCcd944B1D88d0670cae18A00abD272256DDeE",
        challenge_id="1FH5jNuTVIRrPBUNtKrFtQ",
        mint_price=100000000000000,
        default_gas=190000,
    )
    EarthStandsWithCrypto = Mint(
        name="Earth Stands With Crypto",
        mint_address="0xd1E1da0b62761b0df8135aE4e925052C8f618458",
        challenge_id="7JZn2HJuvLZRoE8R8a8OBp",
        mint_price=100000000000000,
        default_gas=190000,
    )
    ShieldingTheWonder = Mint(
        name="Shielding The Wonder",
        mint_address="0x6A3dA97Dc82c098038940Db5CB2Aa6B1541f2ebe",
        challenge_id="7JZn2HJuvLZRoE8R8a8OBp",
        mint_price=100000000000000,
        default_gas=190000,
    )
    NounsStandWithCrypto = Mint(
        name="Nouns Stand With Crypto",
        mint_address="0x03c6eF731453bfEc65a800F83f026ad011D8Abec",
        challenge_id="4JS8wKnPtZ0lE34C5crIUk",
        mint_price=100000000000000,
        default_gas=190000,
    )
    SatoshiSummerRiddle = Mint(
        name="Satoshi's Summer Riddle Pack",
        mint_address="0x24da42FF6C4A6d5a6dCd1BecB204Bf82EA91d7B0",
        challenge_id="6al1rUlphrMNYqQRbG9l83",
        mint_price=650000000000000,
        default_gas=190000,
    )
    LiveAndLetLive = Mint(
        name="Live And Let Live!",
        mint_address="0x279dFFD2b14a4A60e266bEfb0D2c10E695D58113",
        challenge_id="4MMQPGoZviSqLoJgaVDY05",
        mint_price=500000000000000,
        default_gas=190000,
    )
    WeStandWeBuild = Mint(
        name="We stand, we build",
        mint_address="0xEb9A3540E6A3dc31d982A47925d5831E02a3Fe1e",
        challenge_id="43EAydXs7EVNGkR9UZ5JJH",
        mint_price=100000000000000,
        default_gas=190000,
    )
    CryptoVibe = Mint(
        name="Crypto Vibe",
        mint_address="0x6a43B7e3ebFc915A8021dd05f07896bc092d1415",
        challenge_id="OE6zO6T5M3COHSFcIIvmA",
        mint_price=100000000000000,
        default_gas=190000,
    )
    ToshiXSwc = Mint(
        name="Toshi x SWC3",
        mint_address="0xb620bEdCe2615A3F35273A08b3e45e3431229A60",
        challenge_id="1VaefmSAUYw5vW1lxc0Viq",
        mint_price=100000000000000,
        default_gas=190000,
    )
    TheCreativeShield = Mint(
        name="The Creative Shield",
        mint_address="0x892Bc2468f20D40F4424eE6A504e354D9D7E1866",
        challenge_id="6kv6tqF4mCQiGn5SQUwdps",
        mint_price=100000000000000,
        default_gas=190000,
    )
    EnGarde = Mint(
        name="En Garde",
        mint_address="0x1f006edBc0Bcc528A743ee7A53b5e3dD393A1Df6",
        challenge_id="3wnaF1zwkxXMotK2grz0kO",
        mint_price=100000000000000,
        default_gas=190000,
    )
    # Start from here
    LetTheShieldShine = Mint(
        name="Let The Shield Shine",
        mint_address="0x2a8e46E78BA9667c661326820801695dcf1c403E",
        challenge_id="7430li8iAyirOzGFhNbL3w",
        mint_price=100000000000000,
        default_gas=190000,
    )
    AllForOne = Mint(
        name="All for One",
        mint_address="0x8e50c64310b55729F8EE67c471E052B1Cd7AF5b3",
        challenge_id="6ENasd7Ikvs7VBlC02rsCg",
        mint_price=100000000000000,
        default_gas=190000,
    )
    LetsStand = Mint(
        name="Let's Stand",
        mint_address="0x95ff853A4C66a5068f1ED8Aaf7c6F4e3bDBEBAE1",
        challenge_id="66QmTDpn63hpgrkVgRK0ve",
        mint_price=100000000000000,
        default_gas=190000,
    )
    MintTheVision = Mint(
        name="Mint The Vision",
        mint_address="0x8605522B075aFeD48f9987E573E0AA8E572B8452",
        challenge_id="3fYDO7ZCCl91Tg7u6cMHBa",
        mint_price=100000000000000,
        default_gas=190000,
    )
    ForbesWeb3 = Mint(
        name="Forbes Web3 INSPIRE",
        mint_address="0x0821D16eCb68FA7C623f0cD7c83C8D5Bd80bd822",
        challenge_id="ocsChallenge_b3f47fc6-3649-4bad-9e10-7244fbe1d484",
        mint_price=0,
        default_gas=190000,
        type=MintTypes.Claim,
    )
    StandWithCryptoTypography = Mint(
        name="Stand With Crypto Typography",
        mint_address="0x95167eB15a94DD048b2028c8d3fA3490f4cf8c76",
        challenge_id="ocsChallenge_44f5e933-8d23-4757-bbd4-06bf83f922a7",
        mint_price=211000000000000,
        default_gas=190000,
    )
    NatureStandsWithCrypto = Mint(
        name="Nature Stands With Crypto",
        mint_address="0xBB8F6319355d223C4a9f89a1b2A1c183B8Bf4EFF",
        challenge_id="ocsChallenge_7e798e08-31b7-4b8f-b948-7ac7c840ffd7",
        mint_price=100000000000000,
        default_gas=190000,
    )
    YellowInBlue = Mint(
        name="Yellow in blue",
        mint_address="0x74589410924EF2713dE0E769541DfCeCaaa21662",
        challenge_id="ocsChallenge_13fee390-567d-4608-a4ed-9deb156acf8d",
        mint_price=300000000000000,
        default_gas=190000,
    )
    NewWay = Mint(
        name="New Way",
        mint_address="0x674efEb35E7a753a9F015d970B8b580bD509FfCA",
        challenge_id="3JKhK2C1b3rzuIqYUiavJN",
        mint_price=100000000000000,
        default_gas=190000,
    )
    NounsAndCommunity = Mint(
        name="Nouns and Community",
        mint_address="0x227a42Cdbf9Dd3FeB18573d64Da013f8EB203107",
        challenge_id="2HJXu4iu79GaVKPxH7xghW",
        mint_price=100000000000000,
        default_gas=190000,
    )
    ShieldedSerenity = Mint(
        name="Shielded Serenity",
        mint_address="0x8fA00a322665BBA12A738848b11671A0fD5eb7aD",
        challenge_id="3bupOWeKoVFkYR5TKw5jBb",
        mint_price=100000000000000,
        default_gas=190000,
    )
    CryptosDefender = Mint(
        name="Crypto's Defender",
        mint_address="0xACeBBD8e0da95c0DBdc694D844e358aB70353274",
        challenge_id="ccl7qCksXwTejiag1g7M4",
        mint_price=100000000000000,
        default_gas=190000,
    )
    GikosTelescope = Mint(
        name="Giko's Telescope",
        mint_address="0xcB67087f38CC460937e77D6D879acb20663492DF",
        challenge_id="ocsChallenge_1a7f9e88-f4cd-41c3-8de4-a5a5a9c655c7",
        mint_price=300000000000000,
        default_gas=190000,
    )
    TruworldPass = Mint(
        name="Truworld Onchain Pass",
        mint_address="0xf2b0F524e754217905f043A0759d594DA892A59e",
        challenge_id="ocsChallenge_b00cf94a-51aa-4359-abf7-2cada197d0ca",
        mint_price=0,
        default_gas=140000,
        type=MintTypes.ClaimWithId,
        abi=CLAIMABLE_ABI,
    )
    NiceTripToSpace = Mint(
        name="A Nice Trip To Space",
        mint_address="0x849730870b6B9C82E9A8658748bDDD125a537D38",
        challenge_id="ocsChallenge_ce5f1dfd-8e6c-49f8-8246-5f3f2b6a4ec4",
        mint_price=111000000000000,
        default_gas=250000,
    )
    ThankYouForHavingUs = Mint(
        name="Thank You for Having Us",
        mint_address="0xf85fdc5728439105cea9c52baabe3e7cbac36934",
        challenge_id="ocsChallenge_acbbf04b-d703-4ce5-b1ed-32bb461168c7",
        mint_price=777000000000000,
        default_gas=250000,
    )
    SummerBasecampTrek = Mint(
        name="Summer Basecamp Trek",
        mint_address="0x352efbb53972d962a01a9d708c43f5b4510151b6",
        challenge_id="ocsChallenge_15b1524f-de7e-43d5-a9cb-03c9f24d0881",
        mint_price=777000000000000,
        default_gas=250000,
    )

    AllMints = [
        # BaseIsForEveryone,
        # Billboard,
        # BreakingThrough,
        # EthCantBeStopped,
        # Chibling,
        # EtfCelebration,
        # Etfereum,
        # EurcLiveOnBase,
        # HappyBirthdayToshi,
        # MisterMiggles,
        # BuildOnboardAndGrow,
        # TeamLiquid,
        # WelcomeOnchain,
        # WorldAfterEtf,
        # SuperBasedBuilders,
        # SpeedTracker,
        # SeasonalErosion,
        # PixotchiSeed,
        # CityVerse,
        # Summer24,
        # TheThirdNouniversary,
        # CelebratingNouns,
        # BasedNouns,
        # NounsForever,
        # NounsEverywhere,
        # HappyNouniversary,
        # EndOfNounsSzn,
        # NounishVibes,
        # HandOfNouns,
        # MiggsWifNouns,
        # NounifyTheRockies,
        # CoffeeDays,
        # NounsSummerCelebration,
        # NounMoon,
        # WalkingOnSunshine,
        # Consolation,
        # HappyBornThirdDay,
        # BaseTurnsOne,
        # DawnOfDaylight,
        # StixTournamentPass,
        # Strut001,
        # Butterfly,
        # ToshiChess,
        # WatchuLookingAt,
        # Memloop,
        # SummerSerenity,
        # NounsUnderCover,
        # ToshiVibe,
        # ThinkBig,
        # BaseEns,
        # DualityInMotion,
        # StandWithCrypto,
        # StandWithCryptoPizza,
        # StandWithCryptoShield,
        # CryptoWillBloom,
        # StandWithCryptoSong,
        # JuicyAdventure,
        # EspressoAndMilk,
        # PalomarGroup,
        # StandWithCryptoRune,
        # EarthStandsWithCrypto,
        # ShieldingTheWonder,
        # NounsStandWithCrypto,
        # SatoshiSummerRiddle,
        # LiveAndLetLive,
        # WeStandWeBuild,
        # CryptoVibe,
        # ToshiXSwc,
        # TheCreativeShield,
        # EnGarde,
        # LetTheShieldShine,
        # AllForOne,
        # LetsStand,
        # MintTheVision,
        # ForbesWeb3,
        # StandWithCryptoTypography,
        # NatureStandsWithCrypto,
        YellowInBlue,
        NewWay,
        NounsAndCommunity,
        ShieldedSerenity,
        CryptosDefender,
        GikosTelescope,
        TruworldPass,
        NiceTripToSpace,
        ThankYouForHavingUs,
        SummerBasecampTrek,
    ]
