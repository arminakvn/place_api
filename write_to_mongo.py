# client = MongoClient('mongodb://root:' + '67yX8Fuw' + '@146.148.61.119')
# db = client.place_db 
# chica_col = db.chicago_collection
from pymongo import MongoClient

def getMongoColl(db_name, col_name):
    client = MongoClient('mongodb://root:' + '67yX8Fuw' + '@146.148.61.119')
    _db = client[db_name]
    _coll = _db[col_name]
    print "conection to mongo"
    return _coll

def writeMongoDoc(colctn, doc):
    colctn.insert_one(doc)
    return

def writeMongoColl(colctn,lis):
    colctn.insert_many(lis)