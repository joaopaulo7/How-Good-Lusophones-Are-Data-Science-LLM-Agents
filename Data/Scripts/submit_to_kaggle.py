import os
import pandas as pd
import numpy as np
import json
import random
from time import sleep


SUBMISSIONS_DIR = "../Submissions"
FRAMEWORKS = ["explainer-base", "interpreter-base-3tasks"]
LANGUAGES = ["en", "pt"]
MODELS = ["gemini2", "gpt-oss-20b", "qwen3-coder-30b", "gemma3-27b"]


try:
    with open(f"{SUBMISSIONS_DIR}/completed_submissions.json") as in_file:
        completed_submissions = json.load(in_file)
except Exception:
    completed_submissions = []


def submit(competition, file, message):
    if competition+"_"+message in completed_submissions:
        return None
    rsp = os.system(f"kaggle competitions submit {competition} -f {file} -m \"{message}\"")
    if rsp != 0:
        raise Exception("something went wrong with the submission!")
    else: 
        completed_submissions.append(competition+"_"+message)
        with open(f"{SUBMISSIONS_DIR}/completed_submissions.json", 'w') as out_file:
            json.dump(completed_submissions, out_file)
    sleep(abs(random.gauss(45, 20)))


def prepare_submission(framework, language, model):
    model_dir = f"{SUBMISSIONS_DIR}/{framework}/{language}/{model}"
    competitions = os.listdir(model_dir)
    for competition in competitions:
        if language != "en":
            submissions = os.listdir(f"{model_dir}/{competition}/en")
            sub_path = f"{model_dir}/{competition}/en"
        else:
            submissions = os.listdir(f"{model_dir}/{competition}")
            sub_path = f"{model_dir}/{competition}"
                
        for submission in submissions:
            seed = submission.split('_')[1]
            submit(competition, f"{sub_path}/{submission}", f"{framework}_{model}_{language}_{seed}")
                
            
        if len(submissions) < 4:
            completed_seeds = set([submission.split('_')[1] for submission in submissions])
            all_seeds = {f"baseline-{i}" for i in range(4)}
            skipped_seeds = all_seeds - completed_seeds
            for seed in skipped_seeds:
                submit(competition, f"{SUBMISSIONS_DIR}/empty.csv", f"{framework}_{model}_{language}_{seed}")


# make sure empty.csv file exists
with open(f"{SUBMISSIONS_DIR}/empty.csv", "w") as out_file:
    out_file.write("")

for framework in FRAMEWORKS:
    for language in LANGUAGES:
        if language == "pt" and framework == "interpreter-base-3tasks":
            continue
        for model in MODELS:
            prepare_submission(framework, language, model)

