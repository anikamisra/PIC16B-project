from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import InvalidOperation

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Database:
    def __init__(self, db_pswd):
        uri = f"mongodb+srv://Chordy:{db_pswd}@cluster0.pirmgae.mongodb.net/"
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client['cluster0']
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print("db.py initialization error")
            print(e)

    def add_user(self, user: User):
        if self.db.users.find_one({"username": user.username}) is not None:
            return False
        else:
            self.db.users.insert_one(vars(user))
            return True

    def verify_user(self, username, password):
        user = self.db.users.find_one({"username": username})
        if user:
            if user["password"] == password:
                return True
        return False
