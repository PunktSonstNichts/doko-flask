import bcrypt
from doppelkopf import db
from doppelkopf.database_constructors import User


def new_user(username, password):

    if user_already_exist(username):
        return print("user already exist")

    password = password.encode('UTF-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    hashed = hashed.decode("utf-8")

    test = User(username=username, password=hashed)
    db.session.add(test)
    db.session.commit()

    return test


def user_already_exist(username):
    for user in User.query.all():
        print(user.username)
        if user.username == username:
            return True
    return False


def password_check(name, password):

    for user in User.query.all():
        if name == user.username and bcrypt.checkpw(password.encode('UTF-8'), user.password.encode('UTF-8')):
            return True
    return False
