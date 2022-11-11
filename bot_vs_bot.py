import os
import sub_module  # Important, do not remove!

from protossbot.bot import ProtossBot
from sc2.data import Race
from terranbot.bot import TerranBot
from zergbot.bot import ZergBot
from dummies.protoss import *
from dummies.zerg import *
from dummies.terran import *
import random

from sc2.player import Bot

from typing import List

from loguru import logger

# from examples.protoss.warpgate_push import WarpGateBot
# from examples.zerg.zerg_rush import ZergRushBot
from sc2 import maps
from sc2.data import Race, Result
from sc2.main import GameMatch, run_game, run_multiple_games
from sc2.player import Bot


def main_old():
    player1 = "protossbot"
    bots = {
        "tempest": Bot(Race.Protoss, OneBaseTempests()),
        "banshee": Bot(Race.Terran, Banshees()),
        "robo": Bot(Race.Protoss, MacroRobo()),
        "voidray": Bot(Race.Protoss, MacroVoidray()),
        "200roach": Bot(Race.Zerg, MacroRoach()),
        "hydra": Bot(Race.Zerg, RoachHydra()),
        "mutalisk": Bot(Race.Zerg, MutaliskBot()),
        "bc": Bot(Race.Terran, BattleCruisers()),
        "bio": Bot(Race.Terran, BioBot()),
    }

    player2 = random.choice(list(bots.keys()))
    map_name = "AbyssalReefLE"
    result: List[Result] = run_game(
        maps.get(map_name),
        [
            Bot(Race.Protoss, ProtossBot()),
            # Bot(Race.Terran, TerranBot()),
            bots[player2],
            # Bot(Race.Terran, TerranBot()),
        ],
        realtime=False,
        # game_time_limit=2,
        # save_replay_as="Example.SC2Replay",
    )
    logger.info(f"Result: {result}")

    if isinstance(result, Result):
        result_str = result.name
    elif isinstance(result, list):
        result_str = result[0].name
    else:
        result_str = "undefined"

    with open("./results.txt", "a") as output_file:
        output_file.write(f"{player1}  {player2}   {map_name}  {result_str}\n")


# def main():
#     result = run_multiple_games(
#         [
#             GameMatch(
#                 map_sc2=maps.get("AcropolisLE"),
#                 players=[
#                     Bot(Race.Protoss, WarpGateBot()),
#                     Bot(Race.Zerg, ZergRushBot()),
#                 ],
#                 realtime=False,
#                 game_time_limit=2,
#             )
#         ]
#     )
#     logger.info(f"Result: {result}")


if __name__ == "__main__":
    main_old()
    # TODO Why does "run_multiple_games" get stuck?
    # main()