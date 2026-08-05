import os
import shutil
import json
import datetime
from time import sleep

SUBMISSIONS_DIR = "Data/Submissions/explainer-base"
GENERATIONS_DIR = "Data/Generations/explainer-base"
COMPETITIONS_DIR = "Data/Competitions"
WORKSPACE_DIR = "MetaGPT-DataExplainer/workspace"


CURRENT_MODEL = "gemma3-27b"
OLLAMA_MODEL_NAME = "gemma3:27b-it-qat"
SEED_LIST = ["baseline-0", "baseline-1", "baseline-2", "baseline-3"]

LANGUAGES = ["en", "pt"]


try:
    with open("solved_competitions.json") as in_json:
        solved_competitions = json.load(in_json)
except FileNotFoundError:
    solved_competitions = []


def check_solved(language, competition, seed):
    return [language, competition, seed] in solved_competitions

def add_solved(language, competition, seed):
    solved_competitions.append((language, competition, seed))
    with open("solved_competitions.json", "w") as out_json:
        json.dump(solved_competitions, out_json)


def solve_comp(language, competition, competition_info, baseline_prompt, seed, submissions_dir, gen_dir):
    if check_solved(language, competition, seed):
        return None
    
    for file_in_dir in os.listdir(WORKSPACE_DIR):
        if file_in_dir not in ["train.csv", "test.csv"]:
            os.system(f"rm -r {WORKSPACE_DIR}/{file_in_dir}")
    
    os.system(f"ollama stop {OLLAMA_MODEL_NAME}")
    os.system(f"ollama run {OLLAMA_MODEL_NAME} \"\" --keepalive 1h30m")
    
    comp_prompt = baseline_prompt.format(**competition_info)
    output_dir = f"{gen_dir}/{CURRENT_MODEL}/{competition}/{seed}"
    with open("current-comp.json", "w") as out_file:
        json.dump(
            {
                "request": comp_prompt,
                "output_dir": output_dir
            },
            out_file)
    
    os.system("bash run_wrapper.sh")
    
    submission_dir = f"{submissions_dir}/{CURRENT_MODEL}/{competition}"
    os.makedirs(submission_dir, exist_ok=True)
    
    try:
        shutil.copyfile(
            f"{WORKSPACE_DIR}/submission.csv",
            f"{submission_dir}/submission_{seed}_"
                + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                + ".csv")
        
        os.system(f"rm {WORKSPACE_DIR}/submission.csv")
        
    except Exception:
        pass
    add_solved(language, competition, seed)



def solve_per_language(language):
    submissions_dir = f"{SUBMISSIONS_DIR}/{language}"
    gen_dir = f"{GENERATIONS_DIR}/{language}"
    baseline_prompt_file = f"Prompts/base_prompt_{language}.md"
    
    if language == "en":
        train_file = "train.csv"
        test_file = "test.csv"
    else:
        train_file = f"train_{language}.csv"
        test_file = f"test_{language}.csv"


    with open(baseline_prompt_file) as in_md:
        baseline_prompt = in_md.read()

    competitions = []
    for competition in os.listdir(COMPETITIONS_DIR):
        if competition[0:19] == "playground-series-s":
            competitions.append(competition)
    
    for competition in competitions:
        os.system(f"rm -r {WORKSPACE_DIR}/*")
        
        with open(f"{COMPETITIONS_DIR}/{competition}/{language}_info.json") as in_json:
            competition_info = json.load(in_json)
        del competition_info['columns']
        
        shutil.copyfile(
            f"{COMPETITIONS_DIR}/{competition}/{train_file}",
            f"{WORKSPACE_DIR}/train.csv")
        shutil.copyfile(
            f"{COMPETITIONS_DIR}/{competition}/{test_file}",
            f"{WORKSPACE_DIR}/test.csv")
        
        print("=========STARTING COMP===========")
        print(baseline_prompt.format(**competition_info))
        print("=================================")
        for seed in SEED_LIST:
            solve_comp(language, competition, competition_info, baseline_prompt, seed, submissions_dir, gen_dir)
        print("============FINISHED=============")


for language in LANGUAGES:
    solve_per_language(language)

os.system(f"ollama stop {OLLAMA_MODEL_NAME}")
