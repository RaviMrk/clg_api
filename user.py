import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password
    @classmethod
    def find_by_username(self,username):
        connection = sqlite3.connect('data.db')
        cursur = connection.cursor()

        query = "SELECT * FROM user WHERE username=?"
        result = cursur.execute(query, (username,))
        row = result.fetchone()
        if row:
           user = User(*row)    # user = cls(row[0],row[1],row[2])
        else:
            user = None
        
        connection.close()
        return user


    @classmethod
    def find_by_id(self,_id):
        connection = sqlite3.connect('data.db')
        cursur = connection.cursor()

        query = "SELECT * FROM user WHERE id=?"
        result = cursur.execute(query, (_id,))
        row = result.fetchone()
        if row:
           user = User(*row)    # user = cls(row[0],row[1],row[2])
        else:
            user = None
        
        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
    type=str,
    required=True,
    help="This field cannot be blank.")

    parser.add_argument('password',
    type=str,
    required=True,
    help="This field cannot be blank.")

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "A user with that username is already exits"}, 400
        

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO user VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password'],))

        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201

