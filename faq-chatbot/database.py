from pymongo import MongoClient

def get_database():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['faq_db']
    return db

def get_faq_from_db(query):
    db = get_database()
    collection = db['faq_collection']
    faq = collection.find_one({'question': query})
    if faq:
        return faq['answer']
    return None
