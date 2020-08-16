from pymongo import MongoClient

def DB(args):
    db = MongoClient(args.db).get_default_database()
    return db 