from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import bcrypt, DB, session
from flask import flash
import re

class Address:
    def __init__(self,data):
        self.id = data['id']    
        self.street = data['street']
        self.city = data['city']
        self.state = data['state']
        self.zip = data['zip']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def add_address(cls,data):
        query =f"""INSERT INTO addresses ({', '.join(f'{key} 'for key in data)})
                        VALUE ({', '.join(f'%({key})s 'for key in data)})"""

        results = connectToMySQL(DB).query_db(query,data)

        return results
    @classmethod
    def get_address(cls,data):
        query = f"SELECT * FROM addresses WHERE {'and '.join(f'{key} = %({key})s' for key in data)} "

        results =connectToMySQL(DB).query_db(query,data)
        
        if results:
            return cls(results[0])

    @classmethod
    def update_address(self, data,id):
        query = f"""UPDATE addresses SET {', '.join(f'{key} = %({key}' for key in data) }
                            WHERE id = %({id})s """

        results = connectToMySQL(DB).query_db(query,data)
        