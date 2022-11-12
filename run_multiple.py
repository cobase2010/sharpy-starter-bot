import subprocess
import time
import random
import os
import sub_module  # Important, do not remove!
from bot_loader.bot_definitions import BotDefinitions, races, builds, difficulty

root_dir = os.path.dirname(os.path.abspath(__file__))
ladder_bots_path = os.path.join("Bots")
ladder_bots_path = os.path.join(root_dir, ladder_bots_path)
definitions: BotDefinitions = BotDefinitions(ladder_bots_path)

opponents = list(definitions.random_bots.keys())
opponents = [opp for opp in opponents if opp not in ['protossbot', 'zergbot', 'randomprotoss', 'randomzerg', 'randomterran']]
opponents.append('ai')
# opponents = ['mutalisk', 'banshee', 'robo', 'tempest', 'flexbot', 'tank', 'bc', 'lurker', 'hydra']

for n in range(1,100):
    # subprocess.run(f"python run_custom.py -p1 protossbot -p2 {opponent}".split(" "))
    subprocess.run(f"python run_custom.py -p1 protossbot -p2 {random.choice(opponents)}".split(" "))
time.sleep(10)
