import os
import pandas as pd
import numpy as np
from time import sleep

REGRESSION_COMPS = [
    "playground-series-s4e9",
    "playground-series-s4e12",
    "playground-series-s5e2",
    ]

SCORE_FILE = "../Submissions/submission_scores.csv"
LEADERBOARDS_DIR = "../Competitions/leaderboards"

COMPETITIONS = os.listdir("../Competitions")
COMPETITIONS.remove("leaderboards")


# load leaderboards
leaderboards = dict()
for leaderboard_file in os.listdir(LEADERBOARDS_DIR):
    competition = leaderboard_file.split('-publicleaderboard')[0]
    leaderboards[competition] = pd.read_csv(f"{LEADERBOARDS_DIR}/{leaderboard_file}")["Score"].to_numpy()
    

# correct scores
scores_df = pd.read_csv(SCORE_FILE)
scores_df['corrected_score'] = ""
for index in range(len(scores_df)):
    competition = scores_df.loc[index].competition
    score = scores_df.loc[index].publicScore
    
    if competition in REGRESSION_COMPS:
        score = score if score != "" else np.nan
        corr_score = np.sum(leaderboards[competition] >= score)/len(leaderboards[competition])
    else:
        corr_score = np.sum(leaderboards[competition] <= score)/len(leaderboards[competition])
    
    scores_df.at[index, 'corrected_score'] = corr_score

# save corrected csv
scores_df.to_csv(SCORE_FILE)
