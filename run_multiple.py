import subprocess
import time
import random

opponents = ["random"] #, "ai"]
for n in range(1,100):
    # subprocess.run(f"python run_custom.py -p1 protossbot -p2 {opponent}".split(" "))
    subprocess.run(f"python run_custom.py -p1 protossbot -p2 {random.choice(opponents)}".split(" "))
time.sleep(10)
