from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE


class Services :
    def __init__(self,data):
        self.id = data['id']
        self.service_name = data['service_name']
        self.businesses_name = data['businesses_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @classmethod
    def create_services(cls,data):
        query="""
        INSERT INTO services(service_name,businesses_id)Value(%(service_name)s,%(businesses_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)
    @classmethod
    def get_all_service(cls):
        query = """
        SELECT * FROM services
        """
        result = connectToMySQL(DATABASE).query_db(query)
        print(result)
        services = []
        for row in result:
            services.append(cls(row))
        return services
    
    @classmethod
    def get_services_by_business_id(cls, business_id):
        query = """
        SELECT * FROM services where business_id
                """
        result = connectToMySQL(DATABASE).query_db(query)
        if result:
            return cls(result[0])
        else:
            return None


    
    # @classmethod
    # def get_services_by_business_id(cls, data):
    #     query = """
    #     SELECT * FROM services WHERE business_id = %(business_id)s;
    #     """
    #     result = connectToMySQL(DATABASE).query_db(query, data)
    #     services = []
    #     for row in result:
    #         service = cls()
    #         service.id = row['id']
    #         service.service_name = row['service_name']
    #         service.businesses_name = row['businesses_name']
    #         # Set other attributes as needed
    #         services.append(service)
    #     return services

        