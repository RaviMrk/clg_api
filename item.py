from flask_restful import Resource ,reqparse
import sqlite3
from flask_jwt import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be blank!"
                        )

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        else:
            return {'message': 'Item not found'}, 404

    


        # item = next(iter(filter(lambda x: x['name'] == name, items)), None)
        # return {'items': item}

        #return {'item': None}, 200 if item else 404

    @classmethod
    def find_by_name(Cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item' : {'name': row[0], 'price': row[1] }}


    def post(self, name):

        # if next(iter(filter(lambda x: x['name'] == name, items)), None) is not None:
        if self.find_by_name(name):
           return {'meassage': "An item with name'{}' already exits".format(name)}, 400 
        # data = request.get_json()
        data = Item.parser.parse_args()  # gets data from user in json formate parser pass the data
        item = {'name': name, 'price': data['price']}   
        #items.append(item)
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

        return item, 201






    def delete(self, name):
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        return {'message': 'item deleted'}



    def put(self,name):

        data = Item.parser.parse_args()
        item = next(iter(filter(lambda x: x['name'] == name, items)), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        row = result.fetchone()
        connection.close()


        if row:
            return {'item' : {'name': row[0], 'price': row[1] }}
        
        else:
            return {'message': 'Item not found'}, 404