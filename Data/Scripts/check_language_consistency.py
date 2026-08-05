from langdetect import detect_langs, LangDetectException
import nbformat
import os
import pandas as pd


GENERATION_DIR = "../Generations"
LANGUAGES = ["en", "pt"]
MODELS = ["gpt-oss-20b", "qwen3-coder-30b"]


def check_lang(nb_file_path, language, min_prob = 0.95):
    md_correct = 0
    md_texts = 0

    py_correct = 0
    py_texts = 0
    
    nb = nbformat.read(nb_file_path, nbformat.NO_CONVERT)
    for cell in nb.cells:
        cell_type = cell['cell_type']
        source = cell['source']

        if cell_type == "code":
            source = source.splitlines()
            comments = ""
            for text in source:
                if text and text[0:2] == "# ":
                    comments += text[2:] + ". "
            if comments:
                lang = detect_langs(comments)[0]
                if lang.lang == language and lang.prob > min_prob:
                    py_correct += len(comments)
                py_texts += len(comments)
        elif source:
            lang = detect_langs(source)[0]
            if lang.lang == language and lang.prob > min_prob:
                md_correct += len(source)
            md_texts += len(source)
            
    return md_correct/md_texts, py_correct/py_texts, (py_correct + md_correct)/(py_texts + md_texts)



lang_df = pd.DataFrame(columns = ["model", "language", "competition", "seed", "md_cons", "comment_cons", "all_cons"])
for language in LANGUAGES:
    for model in MODELS:
        model_dir = f"{GENERATION_DIR}/{language}/MLE/{model}"
        competitions = os.listdir(model_dir)
        for competition in competitions:
            comp_dir = f"{model_dir}/{competition}"
            for seed in range(4):
                timestamp_dir = f"{comp_dir}/baseline-{seed}/output/{os.listdir(f"{comp_dir}/baseline-{seed}/output")[0]}"
                md_cons, comment_cons, all_cons = check_lang(f"{timestamp_dir}/code.ipynb", language, min_prob=0.95)

                lang_df.loc[len(lang_df)] = [model, language, competition, f"baseline-{seed}", md_cons, comment_cons, all_cons]


lang_df.to_csv(f"{GENERATION_DIR}/language_consistency.csv", index=False)
