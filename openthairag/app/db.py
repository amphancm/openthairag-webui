from pymongo import MongoClient

config={
    "host":"mongo",
    "port":27017,
    "username":"root",
    "password":"123456"
}

class Connection:
    def __new__(cls, database):
        connection=MongoClient(**config)
        return connection[database]
