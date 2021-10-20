import sys

sys.path.append("..")
from logs import LOGGER


def do_drop(bet_type, milvus_cli, mysql_cli):
    try:
        if not milvus_cli.has_collection(bet_type):
            return "collection is not exist"
        status = milvus_cli.delete_collection(bet_type)
        mysql_cli.delete_table(bet_type)
        return status
    except Exception as e:
        LOGGER.error(" Error with  drop table: {}".format(e))
        sys.exit(1)
