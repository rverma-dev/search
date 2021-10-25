import sys

sys.path.append("..")
from logs import LOGGER


def do_count(bet_type, milvus_cli):
    collection_name = bet_type.value+"_001" 
    try:
        if not milvus_cli.has_collection(collection_name):
            return None
        num = milvus_cli.count(collection_name)
        return num
    except Exception as e:
        LOGGER.error(" Error with count table {}".format(e))
        sys.exit(1)
