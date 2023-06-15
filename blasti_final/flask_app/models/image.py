from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app import IMAGES_PATH

class Image :
    def __init__(self,data):
        self.id = data['id']
        self.images = IMAGES_PATH+data['images']
        self.business_id = data['business_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def create_img(cls,data):
        query="""
        INSERT INTO images(images,business_id)Value(%(images)s,%(business_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def get_images_by_business_id(cls,id):
        query="""
        SELECT * FROM images WHERE business_id=%(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,{'id':id})
    

