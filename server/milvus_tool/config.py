import os
from pymilvus import *


MILVUS_HOST = 'localhost'
MILVUS_PORT = 19530

dim = 32
pk = FieldSchema(name='pk', dtype=DataType.INT64, is_primary=True)
field = FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=dim)
schema = CollectionSchema(fields=[pk, field], description="bet_recommendation_gsi")

index_param = {
    "metric_type": "L2",
    "index_type":"IVF_SQ8",
    "params":{"nlist":1024}
    }

top_k = 10
search_params = {
    "metric_type": "L2",
    "params": {"nprobe": 10}
    }
