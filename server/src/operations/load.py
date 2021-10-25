import sys
import os
import time
import numpy as np
import traceback
from functools import reduce
import pandas as pd
from bets import BetType
from ast import literal_eval
from sentence_transformers import SentenceTransformer, util
from sklearn.preprocessing import normalize

sys.path.append("..")
from logs import LOGGER

model = SentenceTransformer('sentence-transformers/paraphrase-distilroberta-base-v2')


# Combine the id of the vector and the question data into a list
def format_data(bookId, title_data, text_data):
    data = []
    for i in range(len(bookId)):
        value = (str(bookId[i]), title_data[i], text_data[i])
        data.append(value)
    return data



# Import vectors to Milvus and data to Redis respectively
def import_data(bet: BetType, file_dir,milvus_cli, redis_cli):       
    collection_name = bet.value+"_001" 
    if bet == BetType.GSI :
        data = pd.read_csv(file_dir,index_col=0,converters={'cuNames': literal_eval})
        id_data = data['gsiId'].tolist()
        #book_data = data['bookName'].tolist()
        title_data = data['gsiName'].tolist()
        text_data = data['cuNames']
        text_data= text_data.str.join(". ").tolist()
        sentence_embeddings = model.encode(title_data)
    else :
        LOGGER.error(" Unsupported bet")
        sys.exit(1)
    sentence_embeddings = normalize(sentence_embeddings)
    # since current dataset is very list inserting without batch
    ids = milvus_cli.insert(collection_name, list(sentence_embeddings), id_data)
    milvus_cli.create_index(collection_name)
    redis_cli.load_data_to_redis(bet.value, data) 
    return len(ids)
