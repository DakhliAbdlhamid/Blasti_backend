from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, EMAIL_REGEX, app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import Flask


class Business :
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.phone = data['phone']
        self.description = data['description']
        self.category_id = data['category_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.bus_list=[]


    @classmethod
    def create_business(cls, data):
        query = """
        INSERT INTO businesses (name, email, password, phone, description, category_id) 
        VALUES (%(name)s,%(email)s, %(password)s, %(phone)s, %(description)s, %(categorie_id)s);
        """
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result


    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM businesses;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        Bisnesses = []
        for row in results:
            Bisnesses.append(cls(row))
        return Bisnesses


    @classmethod
    def get_by_email(cls, data):
        query = """
        SELECT * FROM businesses WHERE email = %(email)s;
        """
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None


    # @classmethod
    # def get_besiness_by_id(cls, data):
    #     query = """
    #     SELECT * FROM businesses WHERE id = %(id)s;
    #     """
    #     result = connectToMySQL(DATABASE).query_db(query,data)
    #     print ("*******",result)
    #     return cls(result[0])
    @classmethod
    def get_besiness_by_id(cls, data):
        query = """
        SELECT * FROM businesses WHERE id = %(id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return cls(result[0])
        else:
            return None

    


    @staticmethod
    def encrypt_string(text):
        encrypted_string = bcrypt.generate_password_hash (text)
        return encrypted_string

    @classmethod
    def delete(cls, data):
        query = """
        delete from businesses where id=%(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)


    @staticmethod
    def validate_business(data):
        is_valid = True
        if len(data['name'])< 3:
            flash("Name must be at least 3", "name" )
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash( "you must provide a valid email", "email" )
            is_valid = False
        if len( data['password'] ) == 0 :
            flash("please provide a passowrd", "password" )
            is_valid = False
        if len(data['password'])< 8:
            flash("Password too short","password" )
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("password de not mach" , "password" )
            is_valid = False
        if Business.get_by_email(data):
            flash ("the email is already taken", "email" )
            is_valid = False
        if len(data['phone'])< 6:
            flash("phone must be at least 6", "phone" )
            is_valid = False
        if len(data['description'])< 10:
            flash("description must be at least 10", "description" )
            is_valid = False
            
        return is_valid
    


#++++++++++++++++++++++++++++++++ added new ++++++++++++
    @classmethod
    def get_business_with_category_by_id(cls, data):
        query = """
        SELECT * FROM businesses
            LEFT JOIN categories ON businesses.category_id = categories.id
            WHERE businesses.category_id = %(id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        print ("***",result)
        bus=[]
        if result:

            this_bus=cls(result[0])
            for row in result:
                bus.append(Business(row))
            this_bus.bus_list=bus
            return bus
        return []
    

    @classmethod
    def get_first_4_businesses(cls):
        query = """
        SELECT * FROM businesses
        LIMIT 4;
        """
        result = connectToMySQL(DATABASE).query_db(query)
        businesses = []
        for row in result:
            businesses.append(cls(row))
        return businesses
    
    # ================get all=====================
    @classmethod
    def get_all_businesses(cls):
        query = """
        SELECT * FROM businesses
        """
        result = connectToMySQL(DATABASE).query_db(query)
        print(result,"$$$$$$$$$$$$$$$$$$$$$$$$$")
        
        businesses = []
        for row in result:
            businesses.append(cls(row))
            
        return businesses


