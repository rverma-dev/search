import os
import time
import sys
import numpy as np
from functools import reduce

from pymilvus.orm import collection

sys.path.append("..")
from config import TOP_K
from logs import LOGGER
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize
from bets import BetType

model = SentenceTransformer('sentence-transformers/paraphrase-distilroberta-base-v2')


def search_in_milvus(bet: BetType, query_sentence, milvus_cli, redis_cli):
    collection_name = bet.value+"_001" 
    try:
        query_embeddings = [query_sentence]
        embed = model.encode(query_embeddings) 
        embed = embed.reshape(1,-1)
        query_embeddings = normalize(embed).tolist()
        LOGGER.info("Successfully insert query list")
        results = milvus_cli.search_vectors(collection_name,query_embeddings,TOP_K)
        vids = [str(x.id) for x in results[0]]
        titles = redis_cli.search_by_milvus_ids(vids, bet.value+"#")
        distances = [x.distance for x in results[0]]
        return titles, distances
    except Exception as e:
        LOGGER.error(" Error with search : {}".format(e))
        sys.exit(1)