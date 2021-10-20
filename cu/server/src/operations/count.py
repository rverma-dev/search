import sys

sys.path.append("..")
from logs import LOGGER


def do_count(bet_type, milvus_cli):
    try:
        if not milvus_cli.has_collection(bet_type):
            return None
        num = milvus_cli.count(bet_type)
        return num
    except Exception as e:
        LOGGER.error(" Error with count table {}".format(e))
        sys.exit(1)
