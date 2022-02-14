import couchdb
import uuid
import bcrypt


def new_user(username, password):
    couch = couchdb.Server('http://admin:1234@localhost:5984/')
    db = couch['loginuser']
    if user_already_exist(username, db):
        return print("already exist")
    password = password.encode('UTF-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    hashed = hashed.decode("utf-8")
    data = {
        '_id': uuid.uuid4().__str__(),
        'username': username,
        'password': hashed
    }
    db.save(data)
    return data


def user_already_exist(username, db):
    for docid in db.view('_all_docs'):
        i = docid['id']
        if db[i]['username'] == username:
            return True
        return False


def password_check(username, password):
    couch = couchdb.Server('http://admin:1234@localhost:5984/')
    db = couch['loginuser']
    for docid in db.view('_all_docs'):
        i = docid['id']
        if db[i]['username'] == username and bcrypt.checkpw(password.encode('UTF-8'), db[i]['password'].encode('UTF-8')):
            return True
    return False



