import os

sql_db = 'sqlite:////tmp/test.db'
HOST = os.environ.get('HOST', 'localhost')
PORT = os.environ.get('PORT', 5002)
