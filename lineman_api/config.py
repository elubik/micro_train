import os

SQL_DB = os.environ.get("SQLALCHEMY_DATABASE_URI", 'sqlite:////tmp/test.db')
HOST = os.environ.get('HOST')
PORT = os.environ.get('PORT', 5002)
