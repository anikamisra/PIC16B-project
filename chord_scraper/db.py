from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import InvalidOperation

class User:
    """
    Represents a user with a username and password.
    """
    def __init__(self, username, password):
        """
        Initializes a User object with the provided username and password.
        Args:
            username (str): The username of the user.
            password (str): The password of the user.
        """
        self.username = username
        self.password = password

class Database:
    """
    Represents a MongoDB database connection.
    """
    def __init__(self, db_pswd):
        """
        Initializes a Database object with the provided MongoDB password.
        Args:
            db_pswd (str): The MongoDB password.
        """
        uri = f"mongodb+srv://Chordy:{db_pswd}@cluster0.pirmgae.mongodb.net/"
        print(uri)
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client['cluster0']
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print("db.py initialization error")
            print(e)

    def add_user(self, user: User):
        """
        Adds a new user to the MongoDB database.
        Args:
            user (User): The User object to be added to the database.
        Returns:
            bool: True if the user is successfully added, False otherwise.
        """
        if self.db.users.find_one({"username": user.username}) is not None:
            return False
        else:
            self.db.users.insert_one(vars(user))
            return True

    def verify_user(self, username, password):
        """
        Verifies the credentials of a user.
        Args:
            username (str): The username to be verified.
            password (str): The password to be verified.
        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        user = self.db.users.find_one({"username": username})
        if user:
            if user["password"] == password:
                return True
        return False
