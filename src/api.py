import sqlite3 
import os

from src.exceptions import DbNotExists
from src.flib       import validate_password
from src.logger     import log



class api:
    DB_ADDR = 'config/users.db'        
    
    def create_users_db(self):
        conn = sqlite3.connect(self.DB_ADDR)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE users (user_name text , user_id text)")
        conn.commit()
        log('Database was created')
    
    def add_user(self , user_name , user_id):
        if os.path.exists(self.DB_ADDR):        
            conn = sqlite3.connect(self.DB_ADDR)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users VALUES (? , ?)" , (user_name , user_id))
            conn.commit()
            
            log('User {0} with id {1} were added'.format(user_name , user_id))
        else:
            raise DbNotExists

    def run(self , args):
        if validate_password():
            if args.get('action') == 'add_new_user':
                if os.path.exists(self.DB_ADDR):
                    if not args.get('user_name'):
                        user_name = 'None'
                    else:
                        user_name = args.get('user_name')
                    self.add_user(user_name , args.get('user_id'))
                else:
                    self.create_users_db()
                    self.add_user(args.get('user_name') , args.get('user_id'))
        else:
            return 'Nothing personal kid'