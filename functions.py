from eth_typing import HexStr
from core import (
    Relay,
    OKX,
    MintFun,
    SpeedTracer,
    SeasonalErosionNFT,
    CoinBasePointsManager,
    CoinbaseMinter,
    BuildersNFT,
    Mints,
    SpinWheel,
    BadgeClaimer,
    SeedNft,
    CityVerseNFT,
    Summer24NFT,
    DayOneNFT,
    Nitro,
    InstantBridge,
    SummerSerenity,
    MemLoop,
    NounsUnderCover,
    BaseName,
    JuicyAdventure,
    PalomarGroup,
    Deploy,
    ANiceTripToSpace,
    ThankYouForHavingUs,
    SummerBasecampTrek,
    TalentProtocol,
    Network,
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
    percentages: tuple[str, str],
    to_network: Network,
):
    relay = Relay(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return relay.bridge(percentages=percentages, to_network=to_network)


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


async def mint_speedtracer(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    speedtracer = SpeedTracer(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return await speedtracer.mint()


def mint_builders(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    mint = BuildersNFT(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return mint.mint()


def mint_seasonal_erosion(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    seasonal_erosion = SeasonalErosionNFT(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return seasonal_erosion.mint()


def mint_welcome(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.WelcomeOnchain)


def check_and_claim_coinbase(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    coinbase = CoinBasePointsManager(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return coinbase.check_and_claim()


def mint_etf(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.EtfCelebration)


def mint_miggles(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.MisterMiggles)


def mint_tl(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.TeamLiquid)


def mint_postetf(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.WorldAfterEtf)


def mint_cbs(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.EthCantBeStopped)


def mint_billboard(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.Billboard)


def spin_wheel_and_trigger_ref(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    wheel = SpinWheel(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return wheel.run_daily_spin()


def mint_badges(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    claimer = BadgeClaimer(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return claimer.run()


def mint_etfereum(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.Etfereum)


def mint_breaking_through(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.BreakingThrough)


def mint_onboard(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.BuildOnboardAndGrow)


def mint_chibling(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.Chibling)


def mint_toshi(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.HappyBirthdayToshi)


def collect_baseforeveryone(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.BaseIsForEveryone)


def mint_eurc_live_on_base(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.EurcLiveOnBase)


def mint_pixotchi(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    pixotchi = SeedNft(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return pixotchi.mint()


def mint_cityverse(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    cityverse = CityVerseNFT(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return cityverse.mint()


def mint_summer(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    summer = Summer24NFT(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return summer.mint()


def mint_nouniversary(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.TheThirdNouniversary)


def mint_celebrating_nouns(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.CelebratingNouns)


def mint_based_nouns(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.BasedNouns)


def mint_nouns_forever(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.NounsForever)


def mint_nouns_everywhere(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.NounsEverywhere)


def mint_happy_nouniversary(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.HappyNouniversary)


def mint_end_of_nouns(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.EndOfNounsSzn)


def mint_nounish_vibes(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.NounishVibes)


def mint_hand_of_nouns(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.HandOfNouns)


def mint_miggs_wif_nouns(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.MiggsWifNouns)


def mint_nounify(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.NounifyTheRockies)


def mint_coffee_days(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.CoffeeDays)


def mint_nouns_summer_celebration(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.NounsSummerCelebration)


def mint_noun_moon(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.NounMoon)


def mint_day_one(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    mint = DayOneNFT(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return mint.mint()


def mint_walking_on_sunshine(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.WalkingOnSunshine)


def mint_consolation(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.Consolation)


def mint_happy_born(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.HappyBornThirdDay)


def mint_base_turns_one(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.BaseTurnsOne)


def mint_dawn_of_daylight(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.DawnOfDaylight)


def mint_stix(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.StixTournamentPass)


def mint_strut(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.Strut001)


def mint_butterfly(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.Butterfly)


def mint_toshi_chess(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.ToshiChess)


def mint_base_canada(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.BaseCanada)


def mint_whatchu_looking_at(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.WatchuLookingAt)


def mint_serenity(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = SummerSerenity(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint()


def mint_memloop(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = MemLoop(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint()


def mint_think_big(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )
    return minter.mint(mint=Mints.ThinkBig)


def mint_toshi_vibe(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )
    return minter.mint(mint=Mints.ToshiVibe)


def mint_nouns_undercover(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = NounsUnderCover(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint()


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


def mint_duality_in_motion(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.DualityInMotion)


def mint_stand_with_crypto(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.StandWithCrypto)


def mint_swc_pizza(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.StandWithCryptoPizza)


def mint_swc_shield(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.StandWithCryptoShield)


def mint_crypto_will_bloom(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.CryptoWillBloom)


def mint_swc_song(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.StandWithCryptoSong)


def mint_juicy_adventure(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):

    minter = JuicyAdventure(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.run()


def mint_espresso(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.EspressoAndMilk)


def mint_palomar(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = PalomarGroup(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint()


def mint_swc_rune(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.StandWithCryptoRune)


def mint_earth_swc(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.EarthStandsWithCrypto)


def mint_shielding_the_wonder(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.ShieldingTheWonder)


def mint_nouns_swc(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.NounsStandWithCrypto)


def mint_satoshi_summer(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.SatoshiSummerRiddle)


def mint_live_let_live(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.LiveAndLetLive)


def mint_stand_build(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.WeStandWeBuild)


def mint_crypto_vibe(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.CryptoVibe)


def mint_toshi_x_swc(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.ToshiXSwc)


def mint_creative_shield(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.TheCreativeShield)


def mint_engarde(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.EnGarde)


def mint_let_the_shield_shine(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.LetTheShieldShine)


def mint_all_for_one(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.AllForOne)


def mint_lets_stand(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.LetsStand)


def mint_vision(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.MintTheVision)


def mint_forbes(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.ForbesWeb3)


def mint_swc_typography(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.StandWithCryptoTypography)


def mint_nature_swc(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.NatureStandsWithCrypto)


def mint_yellow_in_blue(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.YellowInBlue)


def mint_new_way(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.NewWay)


def mint_nouns_and_community(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.NounsAndCommunity)


def mint_shielded_serenity(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.ShieldedSerenity)


def mint_cryptos_defender(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.CryptosDefender)


def mint_giko(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.GikosTelescope)


def mint_truworld_pass(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = CoinbaseMinter(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint(mint=Mints.TruworldPass)


def mint_trip_to_space(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = ANiceTripToSpace(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint()


def mint_thanks(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = ThankYouForHavingUs(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint()


def mint_basecamp_trek(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    minter = SummerBasecampTrek(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return minter.mint()


def bridge_nitro(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
    percentages: tuple[str, str],
    to_network: Network,
):
    nitro = Nitro(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return nitro.bridge(percentages=percentages, to_network=to_network)


def zora_instant_bridge(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
    percentages: tuple[str, str],
):
    instant_bridge = InstantBridge(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return instant_bridge.bridge(percentages=percentages)


def opt_in(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    opt = SpinWheel(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return opt.opt_in()


def check_score(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    score = CoinBasePointsManager(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return score.check_points()


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


def get_ocs_campaign_result(
    account_name: str | int,
    private_key: str | HexStr,
    network: Network,
    user_agent: str,
    proxy: str,
):
    checker = CoinBasePointsManager(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return checker.check_post_ocs_points()


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
