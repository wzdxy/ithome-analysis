import pymongo


class ConnectDb:

    client = pymongo.MongoClient(host='127.0.0.1', port=27017)
    db = client['ithome']
    article = db['article']
    analysis = db['analysis']
