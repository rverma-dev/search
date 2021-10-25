import pandas as pd
from pymongo import MongoClient
import pymongo


def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]


def read_mongo(db, collection, query={}, host='10.220.98.254', port=27017, username='bet', password='bet', no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find().limit(5)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))
    
    # Delete the _id
    if no_id:
        del df['_id']

    return df

def main():
    df = read_mongo(db='nsl_bet_db_soln',collection='nsl_book',query=[{
        '$project': {"nb": "$$ROOT", "_id": 0}
    },
        {
        '$lookup': {
            'localField': "nb.gsiList.id",
            'from': "nsl_gsi",
            'foreignField': "id",
            'as': "ng"
        }
    },
    {
        '$unwind': {
            'path': "$ng",
            'preserveNullAndEmptyArrays': False
        }
    },
    {
        '$lookup': {
            'localField': "ng.solutionLogic.referencedChangeUnit",
            'from': "nsl_change_unit",
            'foreignField': "id",
            'as': "cu"
        }
    },
    {
        '$unwind': {
            'path': "$cu",
            'preserveNullAndEmptyArrays': False
        }
    },
    {
        '$addFields': {"bookId": "$nb.displayName", "gsiId": "$ng.displayName", "bookName": "$nb.displayName", "gsiName": "$ng.displayName", "cuName": "$cu.displayName"}
    },
    {
        '$match': {'$and': [
                {"nb.tenantId": {'$eq': "callhealthdemo"}},
                {"nb.displayName": {'$regex': "^((?!test).)*$", '$options': "i"}},
                {"nb.displayName": {'$regex': "^((?!book).)*$", '$options': "i"}},
                {"ng.displayName": {'$regex': "^((?!test).)*$", '$options': "i"}}
            ]}
    },
    {
        '$group': {
            _id: {"bookId": "$bookId", "gsiId": "$gsiId"},
            "addToSet(cu_name)": {'$addToSet': "$cu.displayName"}
        }
    },
    {
        '$project': {"bookId": "$_id.bookId", "gsiId": "$_id.gsiId", "cuId": "$addToSet(cu_name)", "bookName": "$nb.displayName", "gsiName": "$ng.displayName", "cuName": "$cu.displayName", "_id": 0}
    }])
    df.show


if __name__=="__main__":
    main()