import pandas as pd
import json

COMPETITIONS_DIR = "../Competitions"

def translate_competition(competition):
    
    competition_path = f"{COMPETITIONS_DIR}/{competition}"
    train_path = f"{competition_path}/train.csv"
    test_path = f"{competition_path}/test.csv"
    
    # load competition "dictionary" JSONs
    with open(f"{competition_path}/en_info.json") as en_json:
        en_dict = json.load(en_json)
    
    with open(f"{competition_path}/pt_info.json") as pt_json:
        pt_dict = json.load(pt_json)


    # create translation dictionary
    translation_dic = {"column_translations": {}, "values": []}
    for en_column, pt_column in zip(en_dict['columns'], pt_dict['columns']):
        translation_dic['column_translations'][en_column['column_name']] = pt_column['column_name']
        if en_column['values']:
            aux_val_dic = {"column_name": pt_column['column_name'], "translations": {}}
            for en_value, pt_value in zip(en_column['values'], pt_column['values']):
                aux_val_dic["translations"][en_value] = pt_value
            translation_dic['values'].append(aux_val_dic)

    # load csvs 
    train_csv = pd.read_csv(train_path)
    test_csv = pd.read_csv(test_path)

    # apply translation to csvs
    train_csv_pt = train_csv.rename(columns=(translation_dic['column_translations']))
    test_csv_pt = test_csv.rename(columns=(translation_dic['column_translations']))
    for column in translation_dic['values']:
        train_csv_pt[column['column_name']] = train_csv_pt[column['column_name']].replace(column['translations'])
        
        # ignore target column
        if column['column_name'] in test_csv_pt:
            test_csv_pt[column['column_name']] = test_csv_pt[column['column_name']].replace(column['translations'])

    # save translated csvs
    train_csv_pt.to_csv(train_path, index=False)
    test_csv_pt.to_csv(test_path, index=False)



with open("competitions.json") as in_file:
    competitions = json.load(in_file)

for competition in competitions:
    translate_competition(competition)
