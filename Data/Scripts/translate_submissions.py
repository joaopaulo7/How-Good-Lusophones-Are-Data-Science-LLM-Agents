import pandas as pd
import json
import os

COMPETITIONS_DIR = "../Competitions"
SUBMISSIONS_DIR = "../Submissions"

COMPETITIONS = os.listdir(COMPETITIONS_DIR)
COMPETITIONS.remove("leaderboards")

FRAMEWORKS = ["explainer-base", "interpreter-base-3tasks"]
MODELS = ["gemini2", "gpt-oss-20b", "qwen3-coder-30b", "gemma3-27b"]

def translate_submissions(framework, model, competition):
    with open(f"{COMPETITIONS_DIR}/{competition}/en_info.json") as en_json:
        en_dict = json.load(en_json)
        
    with open(f"{COMPETITIONS_DIR}/{competition}/pt_info.json") as pt_json:
         pt_dict = json.load(pt_json)
    
    # create translation dictionary
    translation_dic = {"column_translations": {}, "values": []}
    for en_column, pt_column in zip(en_dict['columns'], pt_dict['columns']):
        translation_dic['column_translations'][pt_column['column_name']] = en_column['column_name']
        if en_column['values']:
            aux_val_dic = {"column_name": en_column['column_name'], "translations": {}}
            for en_value, pt_value in zip(en_column['values'], pt_column['values']):
                aux_val_dic["translations"][pt_value] = en_value
            translation_dic['values'].append(aux_val_dic)

    submissions_path = f"{SUBMISSIONS_DIR}/{framework}/pt/{model}/{competition}"
    os.makedirs(f"{submissions_path}/en/", exist_ok=True)
    for submission in os.listdir(submissions_path):
        if submission == "en":
            continue
        
        # load csvs 
        submission_csv = pd.read_csv(f"{submissions_path}/{submission}", keep_default_na=False)
        
        # apply translation to csvs
        submission_csv_en = submission_csv.rename(columns=(translation_dic['column_translations']))
        for column in translation_dic['values']:
            # ignore all but target column
            if column['column_name'] in submission_csv_en:
                submission_csv_en[column['column_name']] = submission_csv_en[column['column_name']].replace(column['translations'])
            
            # save translated csvs
            submission_csv_en.to_csv(f"{submissions_path}/en/{submission}", index=False)


for framework in FRAMEWORKS:
    print(f"{framework}:")
    for model in MODELS:
        print(f">{model}:")
        for competition in COMPETITIONS:
            print(f">>{competition}")
            translate_submissions(framework, model, competition)
