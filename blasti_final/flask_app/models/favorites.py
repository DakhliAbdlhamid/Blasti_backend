from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models.business import Business


class Favorites :
    def __init__(self,data):
        self.id = data['id']
        self.business_id=data['business_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorite=Business.get_besiness_by_id({'id':self.business_id})
    @classmethod
    def create_favorites(cls,data):
        query="""
        INSERT INTO favorites(user_id,business_id)Value(%(user_id)s,%(business_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)
    @classmethod
    def get_all_favorites(cls):
        query = """
        SELECT * FROM favorites
        """
        result = connectToMySQL(DATABASE).query_db(query)
        print(result)
        favorites = []
        for row in result:
            favorites.append(cls(row))
        return favorites