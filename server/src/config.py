import os

############### Milvus Configuration ###############
MILVUS_HOST = os.getenv("MILVUS_HOST", "afac1ec1ad6154e69876c8e916ddf9e5-2af2fbf688d30cb6.elb.ap-south-1.amazonaws.com")
MILVUS_PORT = int(os.getenv("MILVUS_PORT", 19530))
VECTOR_DIMENSION = int(os.getenv("VECTOR_DIMENSION", 768))
INDEX_FILE_SIZE = int(os.getenv("INDEX_FILE_SIZE", 1024))
METRIC_TYPE = os.getenv("METRIC_TYPE", "L2")
TOP_K = int(os.getenv("TOP_K", 5))

############### REDIS Configuration ###############
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_PWD = os.getenv("REDIS_PWD", None)

############### MONGO Configuration ###############
MONGO_HOST = os.getenv("MONGO_HOST", "10.220.98.254")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_USER = os.getenv("MONGO_USER", "bet")
MONGO_PWD = os.getenv("MONGO_PWD", "bet@123")
MONGO_DB = os.getenv("MONGO_DB", "nsl_bet_db_soln")

############### Number of log files ###############
LOGS_NUM = int(os.getenv("logs_num", 1))
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
