from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re


class Appointment :
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.service_id = data['service_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def add(cls, data):
        query = """
        INSERT INTO appointments (user_id,service_id,disponibility_id)
        VALUES (%(user_id)s,%(service_id)s,%(disponibility_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    @classmethod
    def delete(cls, data):
        query = """
        delete from appointments where id=%(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    
    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT * FROM appointments WHERE id = %(id)s
        """
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:  # Check if the result is not empty
            return cls(result[0])
        else:
            return None
    @classmethod
    def edit_appointment (cls, data):
        query = """
        UPDATE appointments SET date = %(date)s, description = %(description)s, instructions= %(instructions)s , date = %(date)s, under= %(under)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)
