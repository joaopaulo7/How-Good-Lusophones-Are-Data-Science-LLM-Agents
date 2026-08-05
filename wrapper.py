from asyncio import timeout, TimeoutError, run
import sys
import json
sys.path.insert(0, "MetaGPT-DataExplainer/metagpt")

from metagpt.logs import logger
from metagpt.roles.de.data_explainer import DataExplainer
from metagpt.roles.di.data_interpreter import DataInterpreter
from metagpt.utils.recovery_util import save_history


async def _explain(request, save_dir):
    de = DataExplainer(max_tasks=12)#, markdown_cells=False, toon=True)
    #de = DataInterpreter()
    try:
        async with timeout(7200):
            rsp = await de.run(request)
    except TimeoutError as e:
        rsp = "========TIMEOUT======="
        print("========TIMEOUT=======")
    except Exception as e:
        rsp = "========ERROR======="
        print("========ERROR=======")
    logger.info(rsp)
    save_history(role=de, save_dir=save_dir)

with open("current-comp.json") as in_file:
    in_json = json.load(in_file)


run(_explain(in_json['request'], in_json['output_dir']))
