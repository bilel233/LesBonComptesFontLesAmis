import bcrypt
from flask_mongoengine import MongoEngine

db = MongoEngine()


class User(db.Document):
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)


    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    @classmethod
    def create_user(cls, username, password):
        hashed_password = cls.hash_password(password)
        user = cls(username=username, password=hashed_password)
        user.save()
        return user
