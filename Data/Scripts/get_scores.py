import os
import pandas as pd
import numpy as np
from time import sleep


SUBMISSIONS_DIR = "../Submissions"
FRAMEWORKS = ["explainer-base", "interpreter-base-3tasks"]
LANGUAGES = ["en", "pt"]
MODELS = ["gemini2", "gpt-oss-20b", "qwen3-coder-30b", "gemma3-27b"]

COMPETITIONS = os.listdir("../Competitions")
COMPETITIONS.remove("leaderboards")

REGRESSION_COMPS = [
    "playground-series-s4e9",
    "playground-series-s4e12",
    "playground-series-s5e2",
]

def get_score(framework, competition, model, language, scores_csv):
    for seed in range(4):
        description = f"{framework}_{model}_{language}_baseline-{seed}"
        rows = df[df['description'] == description].sort_values(by="date", ascending=False)
        if not rows.empty and rows.iloc[0]['publicScore'] != "":
            priv_score = rows.iloc[0]['privateScore']
            pub_score = rows.iloc[0]['publicScore']
        else:
            if competition in REGRESSION_COMPS:
                priv_score = np.nan
                pub_score = np.nan
            else:
                priv_score = 0
                pub_score = 0

        scores_csv.loc[len(scores_csv)] = {
            "framework": framework,
            "model": model,
            "competition": competition,
            "language": language,
            "seed": f"baseline-{seed}",
            "privateScore": priv_score,
            "publicScore": pub_score,
            "mean_score" : (float(priv_score) + float(pub_score))/2}


scores_csv = pd.DataFrame(columns=["framework", "model", "competition", "language", "seed", "privateScore", "publicScore"])

# One download call per competition, that's why it's the first loop
for competition in COMPETITIONS:
    if os.system(f"kaggle competitions submissions {competition} -qv > {SUBMISSIONS_DIR}/.temp.csv") != 0:
        continue
    df = pd.read_csv(f"{SUBMISSIONS_DIR}/.temp.csv", keep_default_na=False)
    
    for framework in FRAMEWORKS:
        for model in MODELS:
            for language in LANGUAGES:
                get_score(framework, competition, model, language, scores_csv)


sorted_scores = scores_csv.sort_values(
    by=["framework","model","competition", "language", "seed"],
    ascending=True)
    
sorted_scores.to_csv(f"{SUBMISSIONS_DIR}/submission_scores.csv", index=False)
os.system(f"rm {SUBMISSIONS_DIR}/.temp.csv")
