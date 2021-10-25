import uvicorn
import os
from fastapi import FastAPI, File, UploadFile
from milvus_helpers import MilvusHelper
from redis_helpers import RedisHelper
from logs import LOGGER
from operations.load import import_data
from operations.search import search_in_milvus
from operations.count import do_count
from operations.drop import do_drop
from bets import BetType
import traceback


app = FastAPI()
MILVUS_CLI = MilvusHelper()
REDIS_CLI = RedisHelper()

@app.post('/text/count')
async def count_text(bet: BetType):
    # Returns the total number of titles in the system
    try:
        num = do_count(bet, MILVUS_CLI)
        LOGGER.info("Successfully count the number of entities!")
        return num
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}, 400


@app.post('/text/drop')
async def drop_tables(bet: BetType):
    # Delete the collection of Milvus and Redis
    try:
        status = do_drop(bet, MILVUS_CLI, REDIS_CLI)
        LOGGER.info("Successfully drop tables in Milvus and Redis!")
        return status
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}, 400


@app.post('/text/load')
async def load_text(bet: BetType, file: UploadFile = File(...)):
    try:
        text = await file.read()
        fname = file.filename
        dirs = "data/" + bet.value
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        fname_path = os.path.join(os.getcwd(), os.path.join(dirs, fname))
        with open(fname_path, 'wb') as f:
            f.write(text)
    except Exception as e:
        return {'status': False, 'msg': 'Failed to load data.'}
    # Insert all the docs under the file path to Milvus/betType
    try:
        total_num = import_data(bet, fname_path ,MILVUS_CLI, REDIS_CLI)
        LOGGER.info("Successfully loaded data, total count: {}".format(total_num))
        return "Successfully loaded data!"
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}, 400


@app.get('/text/search')
async def do_search_api(bet: BetType, query_sentence: str = None):
    try:
        title, distances = search_in_milvus(bet,query_sentence, MILVUS_CLI, REDIS_CLI)
        res = []
        for p, d in zip(title, distances):
            dicts = {'title': p, 'similarity':d}
            res+=[dicts]
        LOGGER.info("Successfully searched similar text!")
        return res
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}, 400


if __name__ == "__main__":
    uvicorn.run(app=app, host='0.0.0.0', port=5001)
