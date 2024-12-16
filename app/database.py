
# if want to use sqlalchemy or psycopg
from sqlalchemy import create_engine
import psycopg2
from psycopg2.extras import RealDictCursor
from time import time

from .secrets import db_password
conn_uing_sqlalchemy = True
 

user = 'neondb_owner'

host = 'ep-autumn-voice-a58b57fd.us-east-2.aws.neon.tech'
port = '5432'
database = 'neondb'

# for creating connection string
conn_string = f"postgresql://{user}:{db_password}@{host}:{port}/{database}?sslmode=require"

class db_conn:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance
    
    
    def __init__(self):
        if not hasattr(self, "conn"):
            self.conn = psycopg2.connect(host=host, 
                                            database=database, 
                                            user=user, 
                                            password=db_password, 
                                            cursor_factory=RealDictCursor,
                                        )
            # self.conn = psycopg2.connect(conn_string)
            # self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)


    def get_cursor(self):
        if not hasattr(self, "cursor"):
            try:
                self.cursor = self.conn.cursor()
                
                print("Connection to DB has been successfully established.")
                # self.connection.close()
            except Exception as err:
                print(err)
                return None
        
        return self.cursor
    

    def execute(self, query):
        pass

    
    def close(self):
        self.cursor.close()
        self.conn.close()




"""  sqlalchemy connection9

class db_conn:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, "engine"):
            self.engine = create_engine(conn_string, echo=True)

    def connect(self):
        if not hasattr(self, "connection"):
            try:
                self.connection = self.engine.connect()
                print("Connection to DB has been successfully established.")

                # self.connection.close()
            except Exception as err:
                print(err)
                return None
        
        return self.connection

"""

