from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash, request

class Item:
    db = 'family_list'
    def __init__(self,data):
        self.id = data['id']
        self.item_name = data['item_name']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

# this classmethod works!
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM items JOIN users ON items.user_id = users.id"
        results = connectToMySQL(cls.db).query_db(query)

        all_items = []

        if results:
            for row in results:
                item = cls(row)
                data = {
                    'id':row['id'],
                    'first_name':row['first_name'],
                    'last_name':row['last_name'],
                    'email':row['email'],
                    'password':row['password'],
                    'created_at':row['created_at'],
                    'updated_at':row['updated_at'],
                    'item_name':row['item_name'],
                    'user_id':row['user_id']
                }
                item.creator = user.User(data)
                print("Creator:", item.creator)
                print("Query results:", results)
                print("User data:", data)
                all_items.append(item)
        return all_items

    @classmethod
    def get_one_by_id(cls, data):
        query = "SELECT * FROM items where id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def save(cls,data):
        query = """INSERT INTO items (item_name, user_id) VALUES
        (%(item_name)s, %(user_id)s)"""
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = """UPDATE items SET item_name=%(item_name)s WHERE id=%(id)s
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM items WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_item(item):
        is_valid = True
        # Start of validations
        if len(item['item_name']) < 3:
            flash("Item must have at least 3 characters")
            is_valid = False
        return is_valid

