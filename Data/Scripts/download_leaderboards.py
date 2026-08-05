import os

COMPETITIONS_DIR = "../Competitions"
LEADERBOARDS_DIR = f"{COMPETITIONS_DIR}/leaderboards"

for competition in os.listdir(COMPETITIONS_DIR):
    if competition != "leaderboards":
        os.system(f"kaggle competitions leaderboard -d {competition} -p {LEADERBOARDS_DIR}")
        os.system(f"unzip {LEADERBOARDS_DIR}/{competition}.zip -d {LEADERBOARDS_DIR}")

        os.system(f"rm -r {LEADERBOARDS_DIR}/{competition}.zip")
