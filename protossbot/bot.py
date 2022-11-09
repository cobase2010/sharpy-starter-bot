from random import choice
from typing import Callable, Tuple, List, Dict, Optional

import os
import sys

# This file imports submodules correctly

from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.ability_id import AbilityId
from sharpy.knowledges import KnowledgeBot
from sharpy.managers import ManagerBase
from sharpy.plans.acts.act_base import ActBase
from sharpy.combat.group_combat_manager import GroupCombatManager
from sharpy.managers.core import *
from sharpy.managers.core import ActManager, GatherPointSolver
from sharpy.managers.core import EnemyUnitsManager
from sharpy.managers.extensions import MemoryManager
from sharpy.plans.acts import *
from sharpy.plans.acts.protoss import *
from sharpy.plans.require import *
from sharpy.plans.tactics import *
from sharpy.plans import BuildOrder, Step, SequentialList, StepBuildGas
from sharpy.knowledges import SkeletonBot

# This imports all the usual components for protoss bots
from sharpy.managers.extensions import DataManager, BuildDetector
from sharpy.plans.protoss import *

# This imports all the usual components for terran bots
# from sharpy.plans.terran import *

# This imports all the usual components for zerg bots
# from sharpy.plans.zerg import *

class ProtossBot(KnowledgeBot):
    data_manager: DataManager

    def __init__(self, build_name: str = "default"):
        super().__init__("ProtossSharpyExample")

        self.conceded = False

        self.builds: Dict[str, Callable[[], BuildOrder]] = {
            "zealots": lambda: self.zealot_build(),
            "sentries": lambda: self.sentry_build(),
            "beginner": lambda: self.b2gm_build(),
            "dt_rush": lambda: self.dt_rush_build(),
        }
        build_name = "dt_rush"
        self.build_name = build_name

    def configure_managers(self) -> Optional[List[ManagerBase]]:
        # self.knowledge.roles.role_count = 11

        # Return your custom managers here:
        return [
            MemoryManager(),
            PreviousUnitsManager(),
            LostUnitsManager(),
            EnemyUnitsManager(),
            UnitCacheManager(),
            UnitValue(),
            UnitRoleManager(),
            PathingManager(),
            ZoneManager(),
            BuildingSolver(),
            IncomeCalculator(),
            CooldownManager(),
            GroupCombatManager(),
            GatherPointSolver(),
        ]

    async def create_plan(self) -> BuildOrder:
        if self.build_name == "default":
            self.build_name = choice(list(self.builds.keys()))

        self.data_manager.set_build(self.build_name)
        return self.builds[self.build_name]()

    async def on_step(self, iteration):
        # Optional way to leave the game when losing
        await self.give_up()
        return await super().on_step(iteration)

    async def give_up(self):
        if not self.conceded and self.game_analyzer.been_predicting_defeat_for > 5:
            # sc2ai phrase for leaving the game safely
            await self.chat_send("gg")
            self.conceded = True

        if self.conceded and self.game_analyzer.been_predicting_defeat_for > 10:
            # Leave the game
            self.knowledge.print("Client leaving", "Surrender")
            # await self.client.leave()

    def b2gm_build(self) -> BuildOrder:
        build_steps_probe = [
                Step(
                    None,
                    ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 16), # + 6),
                    skip=UnitExists(UnitTypeId.NEXUS, 2),
                ),
                Step(
                    None, 
                    ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 32+12),
                    skip=UnitExists(UnitTypeId.NEXUS, 3),

                ), # + 12)),
                Step(
                    None, 
                    ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 48+18),
                    # skip=UnitExists(UnitTypeId.NEXUS, 3),

                ), # + 12)),
        ]
        build_steps_buildings = [


        ]
        return BuildOrder(
            # AutoPylon(),
            build_steps_probe,
            Step(Supply(14), GridBuilding(UnitTypeId.PYLON, 1), UnitExists(UnitTypeId.PYLON, 1)),
            Step(Supply(16), GridBuilding(UnitTypeId.GATEWAY, 1)),
            Step(Supply(17), BuildGas(1)),
            Step(Supply(20), Expand(2)),
            Step(Supply(20), GridBuilding(UnitTypeId.CYBERNETICSCORE, 1)),
            Step(Supply(20), BuildGas(2)),
            Step(Supply(22), GridBuilding(UnitTypeId.PYLON, 2), UnitExists(UnitTypeId.PYLON, 2)),
            Step(Supply(23), ProtossUnit(UnitTypeId.STALKER, 3)),
            Step(Supply(23), ChronoUnit(name=UnitTypeId.STALKER, from_building=UnitTypeId.GATEWAY)),
            # Step(Supply(23), ChronoUnit(name=UnitTypeId.ADEPT, from_building=UnitTypeId.CYBERNETICSCORE)),
            Step(Supply(23), Tech(UpgradeId.WARPGATERESEARCH)),
            Step(Supply(23), ChronoTech(AbilityId.RESEARCH_WARPGATE, UnitTypeId.CYBERNETICSCORE)),
            # Step(Supply(25), ChronoUnit(name=UnitTypeId.PROBE, from_building=UnitTypeId.NEXUS)),
            Step(Supply(26), GridBuilding(UnitTypeId.SHIELDBATTERY, 1)),
            Step(Supply(26), GridBuilding(UnitTypeId.ROBOTICSFACILITY, 1)),
            Step(Supply(26), ChronoBuilding(UnitTypeId.ROBOTICSFACILITY)),
            Step(Supply(33), GridBuilding(UnitTypeId.GATEWAY, 3)),
            # Step(Supply(26), GridBuilding(UnitTypeId.SHIELDBATTERY, 1)),
            Step(TechReady(UpgradeId.WARPGATERESEARCH), ProtossUnit(UnitTypeId.STALKER, 6)),
            # Step(Supply(30), ChronoUnit(name=UnitTypeId.PROBE, from_building=UnitTypeId.NEXUS), skip=self.supply_used > 30),
            # Step(Supply(31), GridBuilding(unit_type=UnitTypeId.PYLON, to_count=1, priority=True)),
            Step(UnitReady(UnitTypeId.ROBOTICSFACILITY), ProtossUnit(UnitTypeId.SENTRY, 1)),
            # Step(UnitReady(UnitTypeId.ROBOTICSFACILITY), ProtossUnit(UnitTypeId.OBSERVER, 1)),
            Step(Supply(41), GridBuilding(UnitTypeId.PYLON, 3), UnitExists(UnitTypeId.PYLON, 3)),
            # Step(Supply(41), ChronoUnit(name=UnitTypeId.PROBE, from_building=UnitTypeId.NEXUS)),
            Step(Supply(44), ProtossUnit(UnitTypeId.IMMORTAL, 1)),
            Step(Supply(49), GridBuilding(UnitTypeId.FORGE, 1)),
            Step(Supply(49), ChronoBuilding(UnitTypeId.FORGE)),
            Step(Supply(49), GridBuilding(UnitTypeId.TWILIGHTCOUNCIL, 1)),
            Step(Supply(49), ChronoBuilding(UnitTypeId.TWILIGHTCOUNCIL)),
            Step(UnitReady(UnitTypeId.TWILIGHTCOUNCIL), Tech(UpgradeId.CHARGE)),
            Step(Supply(50), GridBuilding(UnitTypeId.PYLON, 4), UnitExists(UnitTypeId.PYLON, 4)),
            Step(Supply(52), BuildGas(4)),
            Step(Supply(54), ProtossUnit(UnitTypeId.IMMORTAL, 2)),
            Step(Supply(58), GridBuilding(UnitTypeId.PYLON, 5), UnitExists(UnitTypeId.PYLON, 5)),
            Step(Supply(60), Tech(UpgradeId.PROTOSSGROUNDWEAPONSLEVEL1)),
            Step(Supply(60), GridBuilding(UnitTypeId.PYLON, 6), UnitExists(UnitTypeId.PYLON, 6)),
            
            Step(Supply(60), GridBuilding(UnitTypeId.GATEWAY, 6)),
            Step(Supply(60), GridBuilding(UnitTypeId.TEMPLARARCHIVE, 1)),
            Step(Supply(60), ChronoBuilding(UnitTypeId.TEMPLARARCHIVE)),
            Step(Supply(60), GridBuilding(UnitTypeId.PYLON, 7), UnitExists(UnitTypeId.PYLON, 7)),
            Step(Supply(60), ProtossUnit(UnitTypeId.HIGHTEMPLAR, 10), UnitExists(UnitTypeId.ARCHON, 4)),
            Step(Supply(60), Archon([UnitTypeId.HIGHTEMPLAR])),
            Step(Supply(60), ProtossUnit(UnitTypeId.WARPPRISM, 1)),
            Step(Supply(60), ProtossUnit(UnitTypeId.ZEALOT, 100)),
            
            Step(Supply(80), GridBuilding(UnitTypeId.PYLON, 8), UnitExists(UnitTypeId.PYLON, 8)),
            Step(Supply(88), GridBuilding(UnitTypeId.PYLON, 9), UnitExists(UnitTypeId.PYLON, 9)),
            Step(Supply(96), GridBuilding(UnitTypeId.PYLON, 10), UnitExists(UnitTypeId.PYLON, 10)),
            Step(Supply(16), ChronoUnit(name=UnitTypeId.PROBE, from_building=UnitTypeId.NEXUS)),
            Step(Supply(90), AutoPylon()),
            Step(Supply(115), Expand(3)),
            Step(Supply(115), BuildGas(6)),
            Step(Supply(115), Tech(UpgradeId.PROTOSSGROUNDWEAPONSLEVEL2)),
            Step(Supply(115), Tech(UpgradeId.PSISTORMTECH)),
            # AutoPylon(),
            self.create_common_strategy()

        )


    def zealot_build(self) -> BuildOrder:
        # Builds 2 gates and endless wave of zealots
        return BuildOrder(
            Workers(16),
            ChronoBuilding(UnitTypeId.GATEWAY),
            GridBuilding(unit_type=UnitTypeId.PYLON, to_count=1, priority=True),
            GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=2, priority=True),
            Step(UnitExists(UnitTypeId.GATEWAY), AutoPylon()),
            ProtossUnit(unit_type=UnitTypeId.ZEALOT),
            self.create_common_strategy()
        )

    def sentry_build(self) -> BuildOrder:
        return BuildOrder(
            Workers(16),
            ChronoBuilding(UnitTypeId.GATEWAY),
            GridBuilding(unit_type=UnitTypeId.PYLON, to_count=1, priority=True),
            GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=2, priority=True),
            GridBuilding(unit_type=UnitTypeId.CYBERNETICSCORE, to_count=1, priority=True),
            Step(UnitExists(UnitTypeId.GATEWAY), AutoPylon()),
            BuildGas(20),
            ProtossUnit(unit_type=UnitTypeId.SENTRY, priority=True),
            AutoWorker(),
            Expand(10),
            self.create_common_strategy()
        )

    def create_common_strategy(self) -> SequentialList:
         return SequentialList(
             # Sets workers to work
             DistributeWorkers(),
             RestorePower(),
             # Detects enemy units as hallucinations
             PlanHallucination(),
             # Scouts with phoenixes
             HallucinatedPhoenixScout(time_interval=60),
             # Cancels buildings that are about to go down
             PlanCancelBuilding(),
             # Set worker rally point
             WorkerRallyPoint(),
             Step(None, SpeedMining(), lambda ai: ai.client.game_step > 5),
             # Have the combat units gather in one place
             PlanZoneGather(),
             # Defend
             PlanWorkerOnlyDefense(),
             PlanZoneDefense(),
             # Attack, these 2 should be last in a sequential list in this order
            #  Step(UnitExists(UnitTypeId.ARCHON), PlanZoneAttack()),
             PlanZoneAttack(),
             PlanFinishEnemy(),
         )

    def dt_rush_build(self) -> BuildOrder:
        self.building_solver.wall_type = 2  # WallType.ProtossMainZerg

        build_steps_buildings2 = [
            Step(UnitReady(UnitTypeId.GATEWAY, 1), GridBuilding(UnitTypeId.CYBERNETICSCORE, 1)),
            Step(UnitReady(UnitTypeId.CYBERNETICSCORE, 1), GridBuilding(UnitTypeId.TWILIGHTCOUNCIL, 1)),
            Step(UnitReady(UnitTypeId.TWILIGHTCOUNCIL, 1), GridBuilding(UnitTypeId.DARKSHRINE, 1)),
            Tech(UpgradeId.BLINKTECH),
            Tech(UpgradeId.CHARGE),
        ]

        build_steps_workers = [
            Step(None, ActBuilding(UnitTypeId.NEXUS, 1), UnitExists(UnitTypeId.NEXUS, 1)),
            # Build to 14 probes and stop until pylon is building
            Step(None, ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS), UnitExists(UnitTypeId.PROBE, 14)),
            Step(None, None, UnitExists(UnitTypeId.PYLON, 1)),
            Step(None, ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS), UnitExists(UnitTypeId.PROBE, 16 + 3 + 3)),
            Step(RequireCustom(lambda k: self.zone_manager.own_main_zone.minerals_running_low), Expand(2)),
            Step(None, ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS), UnitExists(UnitTypeId.PROBE, 30)),
            GridBuilding(UnitTypeId.GATEWAY, 5),
            BuildGas(3),
            GridBuilding(UnitTypeId.GATEWAY, 6),
        ]

        build_steps_buildings = [
            Step(Supply(14), GridBuilding(UnitTypeId.PYLON, 1), UnitExists(UnitTypeId.PYLON, 1)),
            StepBuildGas(1, Supply(16)),
            Step(Supply(16), GridBuilding(UnitTypeId.GATEWAY, 1)),
            BuildGas(2),
            Step(Supply(21), GridBuilding(UnitTypeId.PYLON, 2), UnitExists(UnitTypeId.PYLON, 2)),
            GridBuilding(UnitTypeId.GATEWAY, 2),
            Step(UnitReady(UnitTypeId.CYBERNETICSCORE, 1), Tech(UpgradeId.WARPGATERESEARCH)),
            GridBuilding(UnitTypeId.GATEWAY, 3),
            AutoPylon(),
        ]

        build_steps_units = [
            Step(
                None,
                ProtossUnit(UnitTypeId.DARKTEMPLAR, 4, priority=True),
                skip_until=UnitReady(UnitTypeId.DARKSHRINE, 1),
            ),
            Step(
                UnitReady(UnitTypeId.GATEWAY, 1),
                # ChronoUnit(UnitTypeId.ZEALOT, UnitTypeId.GATEWAY),
                ProtossUnit(UnitTypeId.ZEALOT, 1),
                TechReady(UpgradeId.WARPGATERESEARCH, 1),
            ),
            Step(None, ProtossUnit(UnitTypeId.SENTRY, 1), skip_until=UnitExists(UnitTypeId.STALKER, 3)),
            Step(None, ProtossUnit(UnitTypeId.OBSERVER, 1), skip_until=UnitExists(UnitTypeId.STALKER, 3)),
            Step(None, ProtossUnit(UnitTypeId.STALKER), None),
        ]
        build_steps_units2 = [
            Step(
                UnitExists(UnitTypeId.TWILIGHTCOUNCIL, 1),
                ProtossUnit(UnitTypeId.STALKER, 3),
                TechReady(UpgradeId.WARPGATERESEARCH, 1),
            ),
            Step(Minerals(400), ProtossUnit(UnitTypeId.ZEALOT)),
        ]

        build_steps_chrono = [
            Step(
                None,
                ChronoUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS),
                skip=UnitExists(UnitTypeId.PROBE, 20, include_killed=True),
                skip_until=UnitReady(UnitTypeId.PYLON),
            ),
            Step(
                None,
                ChronoUnit(UnitTypeId.STALKER, UnitTypeId.GATEWAY),
                skip=UnitExists(UnitTypeId.STALKER, 3, include_killed=False),
                # skip_until=UnitReady(UnitTypeId.PYLON),
            ),
            
            ChronoAnyTech(0),
        ]

        build_order = BuildOrder(
            [
                build_steps_buildings,
                build_steps_buildings2,
                build_steps_workers,
                build_steps_units,
                build_steps_units2,
                build_steps_chrono,
            ]
        )

        attack = PlanZoneAttack(20)
        attack.retreat_multiplier = 0.5  # All in

        tactics = [
            PlanCancelBuilding(),
            PlanZoneDefense(),
            RestorePower(),
            DistributeWorkers(),
            Step(None, SpeedMining(), lambda ai: ai.client.game_step > 5),
            # Detects enemy units as hallucinations
            PlanHallucination(),
            # Scouts with phoenixes
            HallucinatedPhoenixScout(time_interval=60),
            DarkTemplarAttack(),
            PlanZoneGather(),
            attack,
            PlanFinishEnemy(),
        ]

        return BuildOrder(build_order, tactics)