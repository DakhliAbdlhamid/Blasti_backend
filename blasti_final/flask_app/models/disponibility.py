from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash


class Disponibility :
    def __init__(self,data):
        self.id = data['id']
        self.day = data['day']
        self.start_time = data['start_time']
        self.end_time = data['end_time']
        self.day = data['day']
        

#                                    Query
    @classmethod
    def create_disponibility(cls,data):
        query="""
        INSERT INTO disponibility(day,start_time,end_time,businesses_id) VALUES (%(day)s,%(start_time)s,%(end_time)s,%(businesses_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)



    @classmethod
    def get_all_disponibility(cls,data):
        query = """
        SELECT * FROM disponibility WHERE business_id=%(id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        disponibilities = []
        for row in result:
            disponibilities.append(cls(row))
        return disponibilities
    
    @classmethod
    def get_disponibility_by_id(cls,data):
    
        query = """
        SELECT * FROM disponibility WHERE id=%(id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return cls(result[0])
        else:
            return None

    @staticmethod
    def validate_disponibility(data):
        is_valid = True
        # Perform validation checks
        if len(data['start_time']) == 0 or len(data['end_time']) == 0:
            is_valid = False
            flash("Start time and end time are required.", "disponibility")
        # Add more validation checks as needed
        
        return is_valid