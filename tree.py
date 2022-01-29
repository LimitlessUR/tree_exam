from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from ..models.user import User


class Tree:
    db_name = 'tree'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.species = db_data['species']
        self.location = db_data['location']
        self.reason = db_data['reason']
        self.date = db_data['date']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.planter = None
        self.visitor= []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO trees (species, location, reason, date, user_id) VALUES (%(species)s,%(location)s,%(reason)s,%(date)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM trees;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_trees = []
        for row in results:
            all_trees.append( cls(row) )
        return all_trees
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM trees WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE trees SET species=%(species)s, location=%(location)s, reason=%(reason)s, date=%(date)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM trees WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def visitor(cls,data):
        query = "INSERT INTO visitors (user_id, tree_id) values (%(user_id)s, %(tree_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

#SELECT * FROM trees left join users on users.id = trees.user_id left join visitors on trees.id = visitors.tree_id left join users as visitor on visitors.id = visitors.user_id;

    @classmethod
    def user_visitors(cls):
        query = "SELECT * FROM trees left join users on users.id = trees.user_id left join visitors on trees.id = visitors.tree_id left join users as visitor on visitors.id = visitors.user_id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results) 
        all_trees = []
        
        for row in results:

            new_tree = True
            
            v_data = {
                "id":row['visitor.id'],
                "first_name":row['visitor.first_name'],
                "last_name":row['visitor.last_name'],
                "email":row['visitor.email'],
                "password":row['visitor.password'],
                "created_at":row['visitor.created_at'],
                "updated_at":row['visitor.updated_at']   
            }
            if len(all_trees)>0 and all_trees[len(all_trees)-1].id == row['id']:
                all_trees[len(all_trees)-1].visitor.append(User(v_data))
                
                new_tree = False
            if new_tree:
                this_tree = cls(row)

                planter_data = {
                "id":row['users.id'],
                "first_name":row['first_name'],
                "last_name":row['last_name'],
                "email":row['email'],
                "password":row['password'],
                "created_at":row['users.created_at'],
                "updated_at":row['users.updated_at'] 
                }
                this_planter = User(planter_data)

                this_tree.planter = this_planter

                if row['visitor.id'] is not None:
                
                    this_tree.visitors.append(user.User(p_data))
                all_trees.append(this_tree)
        return all_trees    



    @staticmethod
    def validate_tree(tree):
        is_valid = True
        if len(tree['species']) < 3:
            is_valid = False
            flash("species must be at least 3 characters","tree")
        if len(tree['location']) < 3:
            is_valid = False
            flash("model must be at least 3 characters","tree")
        if len(tree['reason']) < 3:
            is_valid = False
            flash("make must be at least 3 characters","tree")
        if tree['date'] == "":
            is_valid = False
            flash("Please enter a date","tree")
        
        return is_valid