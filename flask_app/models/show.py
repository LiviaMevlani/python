from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Show:
    db_name = 'userspython2024'
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.user_id = data['user_id']



    @classmethod
    def create(cls, data):
        query = "INSERT INTO shows (title, network, release_date, description, user_id) VALUES ( %(title)s, %(network)s, %(release_date)s, %(description)s,  %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def getAllShows(cls):
        query = "SELECT * FROM shows;"
        results = connectToMySQL(cls.db_name).query_db(query)
        shows = []
        if results:
            for show in results:
                shows.append(show)
        return shows
    
    @classmethod
    def get_logged_shows(cls,data):
        query = "SELECT * FROM shows where users_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        shows = []
        if results:
            for show in results:
                shows.append(show)
        return shows
    

    
    
    @classmethod
    def get_show_by_id(cls, data):
        query = "SELECT * FROM shows left join users on shows.user_id = users.id where shows.id = %(show_id)s;"
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    
    @classmethod
    def delete_show(cls, data):
        query = "DELETE FROM shows WHERE id= %(show_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def update_show(cls, data):
        query = "UPDATE shows SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s  WHERE id = %(id)s ;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_users_show(cls, data):
        query = "delete from shows where shows.user_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def addLike(cls,data):
        query = "INSERT INTO likes (user_id, show_id) VALUES (%(id)s, %(show_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def removeLike(cls,data):
        query = "DELETE FROM likes where show_id = %(show_id)s and user_id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    
    @classmethod
    def get_likers(cls, data):
        query = "SELECT user_id from likes where likes.show_id = %(show_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        likers = []
        if results:
            for person in results:
                likers.append(person['user_id'])
        return likers
    
    @classmethod
    def get_likers_info(cls, data):
        query = "SELECT * from likes left join users on likes.user_id = users.id where likes.show_id = %(show_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        likers = []
        if results:
            for person in results:
                likers.append(person)
        return likers



    @classmethod
    def delete_all_likes(cls,data):
        query = "DELETE FROM likes where show_id = %(show_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_show(data):
        is_valid = True
        # test whether a field matches the pattern
        if len(data['title']) < 3:
            flash("Title should be at least 3 characters!", 'title')
            is_valid = False
        if len(data['network']) < 3:
            flash("The network should be at least 3 characters!", 'network')
            is_valid = False
        if not data['release_date']:
            flash("The year that the movie was released is required!", 'release_date')
            is_valid = False
        if not data['description']:
            flash("The description is required!", 'description')
            is_valid = False
        return is_valid
    