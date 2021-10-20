import enum
import uvicorn
import sys
import os
import os.path as path
from logs import LOGGER
from fastapi import FastAPI, File, UploadFile
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
import numpy as np
from milvus_helpers import MilvusHelper
from redis_helpers import RedisHelper
from operations.load import import_data
from operations.search import search_in_milvus
from operations.count import do_count
from operations.drop import do_drop
from typing import Optional
from enum import Enum


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])
MILVUS_CLI = MilvusHelper()
REDIS_CLI = RedisHelper()

class BetType(Enum):
    CU = 'cu#'
    GSI = 'gsi#'


@app.post('/text/count')
async def count_text(table_name: str = None):
    # Returns the total number of titles in the system
    try:
        num = do_count(table_name, MILVUS_CLI)
        LOGGER.info("Successfully count the number of entities!")
        return num
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}, 400


@app.post('/text/drop')
async def drop_tables(table_name: str = None):
    # Delete the collection of Milvus and Redis
    try:
        status = do_drop(table_name, MILVUS_CLI, REDIS_CLI)
        LOGGER.info("Successfully drop tables in Milvus and MySQL!")
        return status
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}, 400


@app.post('/text/load')
async def load_text(file: UploadFile = File(...), table_name: str = None):
    try:
        text = await file.read()
        fname = file.filename
        dirs = "data"
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        fname_path = os.path.join(os.getcwd(), os.path.join(dirs, fname))
        with open(fname_path, 'wb') as f:
            f.write(text)
    except Exception as e:
        return {'status': False, 'msg': 'Failed to load data.'}
    # Insert all the image under the file path to Milvus/MySQL
    try:
        total_num = import_data(table_name, fname_path ,MILVUS_CLI, REDIS_CLI)
        LOGGER.info("Successfully loaded data, total count: {}".format(total_num))
        return "Successfully loaded data!"
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}, 400


@app.get('/text/search')
async def do_search_api(table_name: str = None, query_sentence: str = None):
    try:
        ids,title, text, distances = search_in_milvus(table_name,query_sentence, MILVUS_CLI, REDIS_CLI)
        res = []
        for p, d in zip(title, text):
            dicts = {'title': p, 'content':d}
            res+=[dicts]
        LOGGER.info("Successfully searched similar text!")
        return res
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}, 400


if __name__ == "__main__":
    uvicorn.run(app=app, host='0.0.0.0', port=5001)
