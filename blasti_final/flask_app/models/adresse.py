from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash


class Adresse :
    def __init__(self,data):
        self.id = data['id']
        self.country = data['country']
        self.state = data['state']
        self.city = data['city']
        self.street = data['street']
        self.postal_code = data['postal_code']
        self.businesses_id = data['businesses_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create_adresse(cls, data):
        print("/:/:/:/:/:/:/:/:/:/:/:/:/:/:/:/:/:/:/:/:/:/Creating address with data:", data)  # Add this line for debugging
        query = """
        INSERT INTO adresses (country, state, city, street, postal_code, businesses_id) 
        VALUES (%(country)s,%(state)s, %(city)s, %(street)s, %(postal_code)s, %(businesses_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)


    @classmethod
    def get_adresse_by_id(cls, data):
        query = """
        SELECT * FROM adresses WHERE id = %(id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        if result:
            return cls(result[0])
        else:
            return None


    @staticmethod
    def validate_adresses(data):
        is_valid = True
        if len(data['country'])< 3:
            flash("country must be at least 3", "country" )
            is_valid = False
        if len(data['state'])< 3:
            flash("state must be at least 3", "state" )
            is_valid = False
        if len(data['city'])< 3:
            flash("city must be at least 3", "city" )
            is_valid = False
        if len(data['street'])< 3:
            flash("street must be at least 3", "street" )
            is_valid = False
        if len(data['postal_code'])< 3:
            flash("postal_code must be at least 3", "postal_code" )
            is_valid = False
        return is_valid 