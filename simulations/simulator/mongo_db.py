import pymongo

client = pymongo.MongoClient()


def get_db():
    return client['simulations']


def save_snapshot(db, simulation_id, simulation_data):
    if simulation_id not in db.list_collection_names():
        db.create_collection(simulation_id)
    db[simulation_id].insert_one(simulation_data)


def get_simulation_snapshot(db, simulation_id, step):
    collection = db[simulation_id]
    return collection.find_one({"step": step})
