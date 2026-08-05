import nbformat
import json
import os
from openai import OpenAI


with open("llm_config.json") as in_file:
    config_json = json.load(in_file)
    llm_creds = config_json['creds']
    llm_config = config_json['config']
        
llm_client = OpenAI(**llm_creds)

with open("../Prompts/describe_image_en.md") as in_file:
    sys_prompt = in_file.read()


def get_image_description(image):
    response = llm_client.chat.completions.create(
        **llm_config,
        messages=[
            {"role": "system", "content": sys_prompt},
            {
                "role": "user",
                "content":
                [{
                    "type": "image_url",
                    "image_url": {
                        "url":  f"data:image/png;base64,{image}"
                    }
                }]
            }
        ]
    )
    return response.choices[0].message.content

def get_md(nb):
    nb_md = ""
    
    for cell in nb.cells:
        if cell['cell_type'] == 'markdown':
            nb_md += cell['source'] + "\n"
        elif cell['cell_type'] == 'code':
            nb_md += "\n```output\n"
            for output in cell['outputs']:
                if output['output_type'] == "stream":
                    nb_md += output['text'] + "\n"
                elif output['output_type'] == "display_data":
                    image = output['data']['image/png']
                    nb_md += "IMAGE:" #+ get_image_description(image) + "\n\n"
            nb_md += "```\n"
    
    return nb_md


paths = []
nbs = []
for language in os.listdir("Generations"):
    language_path = "Generations/"+language+"/EDA/"
    for eda_model in os.listdir(language_path):
        eda_model_path = language_path+eda_model
        for competition in os.listdir(eda_model_path):
            competition_path = eda_model_path+"/"+competition
            latest_output = sorted(os.listdir(competition_path+"/output"), reverse=True)[0]
            
            nb = nbformat.read(competition_path+"/output/"+latest_output+"/code.ipynb", as_version=nbformat.NO_CONVERT)
            paths.append(competition_path)
            nbs.append(nb)
            
for path, nb in zip(paths, nbs):
    with open(path+"/transcript.md", "w") as out_md:
        out_md.write(get_md(nb))
