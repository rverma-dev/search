import sys

sys.path.append("..")
from logs import LOGGER


def do_drop(bet_type, milvus_cli, redis_cli):
    collection_name = bet_type.value+"_001" 
    try:
        if not milvus_cli.has_collection(collection_name):
            print('skip milvus')
            #return "collection is not exist"
        #status = milvus_cli.delete_collection(collection_name)
        redis_cli.delete_all_data(bet_type.value + "#")
        return "status"
    except Exception as e:
        LOGGER.error(" Error with  drop table: {}".format(e))
        sys.exit(1)
