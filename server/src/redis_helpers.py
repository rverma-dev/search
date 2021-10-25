import redis
import sys
import json
from config import REDIS_HOST, REDIS_PORT, REDIS_PWD
from logs import LOGGER

class RedisHelper():
    def __init__(self):
        self.conn = redis.StrictRedis(
            host=REDIS_HOST, port=REDIS_PORT)

    def test_connection(self):
        try:
            self.conn.ping()
        except:
            self.conn = redis.StrictRedis(
                host=REDIS_HOST, port=REDIS_PORT)

    # Batch insert (Milvus_ids, bet data) to redis
    def load_data_to_redis(self, key_prefix, data ):
        self.test_connection()
        # 0|Health insurance_377|CustomerPortal_HealthInsurance|['Customer Menu Options', 'Customer Accessing Portal']
        try:
            pipe = self.conn.pipeline()
            for i in range(len(data['gsiId'])):
                pipe.set('{}#{}'.format(key_prefix, int(data['gsiId'][i])), data['gsiName'][i])
                pipe.execute()
        except Exception as e:
            LOGGER.error("Redis ERROR: {} with bulk insert: {}".format(e,data['gsiId'][0]))
            sys.exit(1)

    # Get the bet data according to the milvus ids
    def search_by_milvus_ids(self, ids, key_prefix):
        self.test_connection()
        keys = [key_prefix + x for x in ids]
        try:
            return self.conn.mget(keys)
        except Exception as e:
            LOGGER.error("Redis ERROR: {} with lookup, key: {}".format(e, keys))
            sys.exit(1)

    # Delete redis key if exists
    def delete_keys(self, ids, key_prefix):
        self.test_connection()
        keys = [key_prefix + x for x in ids]
        try:
            self.conn.delete(keys)
        except Exception as e:
            LOGGER.error("Redis ERROR: {} with deleteion, key: {}".format(e, keys))
            sys.exit(1)

    # Delete all the data in redis db by bet type
    def delete_all_data(self, key_prefix):
        self.test_connection()
        scan_count = redis.register_script(
            """
            local result = redis.call('SCAN', ARGV[1], 'MATCH', ARGV[2], 'COUNT', ARGV[3])
            result[2] = #result[2]
            return result
            """
        )
        pattern = key_prefix + '*'
        cursor = '0'
        try:
            cursor, count = scan_count(args=["0", pattern, 100])
            while cursor != "0":
                cursor, count_delta = scan_count(args=[cursor, pattern, 100])
                count += count_delta
            return count
        except Exception as e:
            LOGGER.error("Redis ERROR: {} with drop, bet: {}".format(e,key_prefix))
            sys.exit(1)

    # Get the number of redis table
    def count_bets(self, betType):
        self.test_connection()
        """Counts the number of keys matching a pattern.
        Doesn't use the redis KEYS command, which blocks and therefore can create availability
        problems.
        Instead of using SCAN and then counting the resulting keys, runs the SCAN via a lua script and
        counts the keys on the redis side, just to save bandwidth.
        We can't implement the entire scan loop in lua, because then it would block just as much as
        KEYS, because the entire lua script runs atomically.
        """
        scan_count = redis.register_script(
            """
            local result = redis.call('SCAN', ARGV[1], 'MATCH', ARGV[2], 'COUNT', ARGV[3])
            result[2] = #result[2]
            return result
            """
        )
        pattern = betType + '*'
        cursor = '0'
        try:
            cursor, count = scan_count(args=["0", pattern, 100])
            while cursor != "0":
                cursor, count_delta = scan_count(args=[cursor, pattern, 100])
                count += count_delta
            return count
        except Exception as e:
            LOGGER.error("Redis ERROR: {} with count all, pattern: {}".format(e, pattern))
            sys.exit(1)
