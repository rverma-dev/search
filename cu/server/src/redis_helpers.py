import redis
import sys
import json
from config import REDIS_HOST, REDIS_PORT, REDIS_PWD
from logs import LOGGER

class RedisHelper():
    def __init__(self):
        self.conn = redis.StrictRedis(
            host=REDIS_HOST, port=REDIS_PORT, auth=REDIS_PWD)

    def test_connection(self):
        try:
            self.conn.ping()
        except:
            self.conn = redis.StrictRedis(
                host=REDIS_HOST, port=REDIS_PORT, auth=REDIS_PWD)

    # Batch insert (Milvus_ids, bet data) to redis
    def load_data_to_redis(self, data, betType):
        self.test_connection()
        # 0|Health insurance_377|CustomerPortal_HealthInsurance|['Customer Menu Options', 'Customer Accessing Portal']
        try:
            pipe = self.conn.pipeline()
            for i in range(len(data['gsiId'])):
                temp = {"gsi": data['gsiName'][i], "cus": data['cuNames'][i]}
                pipe.set(betType + int(data['gsiId'][i]), json.dumps(temp))
                pipe.execute()
        except Exception as e:
            LOGGER.error("Redis ERROR: {} with bulk insert: {}".format(e,data['gsiId'][0]))
            sys.exit(1)

    # Get the bet data according to the milvus ids
    def search_by_milvus_ids(self, ids, betType):
        self.test_connection()
        key = betType + ids
        try:
            return self.conn.get(key)
        except Exception as e:
            LOGGER.error("Redis ERROR: {} with lookup, key: {}".format(e, key))
            sys.exit(1)

    # Delete redis table if exists
    def delete_keys(self, ids, betType):
        self.test_connection()
        key = betType + ids
        try:
            self.conn.delete(key)
        except Exception as e:
            LOGGER.error("Redis ERROR: {} with deleteion, key: {}".format(e, key))
            sys.exit(1)

    # Delete all the data in redis db by bet type
    def delete_all_data(self, betType):
        self.test_connection()
        pattern = betType + '*'
        cursor = '0'
        try:
            cursor, data = self.conn.scan(cursor, pattern, 100)
            for key in data:
                self.conn.delete(key)
        except Exception as e:
            LOGGER.error("Redis ERROR: {} with drop, bet: {}".format(e,betType))
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
