from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Category :
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        

    @classmethod
    def get_all(cls):
        # Your Code here
        pass

    @classmethod
    def get_categorie_by_id(cls, data):
        query = """
        SELECT * FROM categories WHERE id = %(id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        print (result)
        return cls(result[0])
    @classmethod
    def get_all_categories(cls):
        query = """
        SELECT * FROM categories
        """
        result = connectToMySQL(DATABASE).query_db(query)
        print(result)
        categories = []
        for row in result:
            categories.append(cls(row))
        return categories
    




# ========================= new categories =========================



#                               Query

    @classmethod
    def add_category(cls, data):
        query = """
        INSERT INTO category (name)
        VALUES (%(name));
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    def __repr__(self) -> str:
        return f"{self.name}"

    @classmethod
    def get_first_categories(cls):
        query = """
        SELECT * FROM categories
        LIMIT 4
        """
        result = connectToMySQL(DATABASE).query_db(query)
        print(result)
        categories = []
        for row in result:
            categories.append(cls(row))
        return categories


    @classmethod
    def get_all_categories(cls):
        query = """
        SELECT * FROM categories
        """
        result = connectToMySQL(DATABASE).query_db(query)
        print(result)
        categories = []
        for row in result:
            categories.append(cls(row))
        return categories
    
    @classmethod
    def get_category_by_id(cls, data):
        query = """
        SELECT * FROM categories where id = %(id)s
        """
        result = connectToMySQL(DATABASE).query_db(query, data)
        print(result)
        return cls(result[0])