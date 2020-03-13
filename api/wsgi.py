import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db_conn = 'postgres://nuhjrbye:fZ5gd1PqRaBJdx9MUUW0H3KaswyE5_Oi@drona.db.elephantsql.com:5432/nuhjrbye'
# db_conn = 'postgres://admin:12345678@db/bills'
app.config['SQLALCHEMY_DATABASE_URI'] = db_conn
db = SQLAlchemy(app)
app.secret_key = b'yhb77sw9_"F4Q8z\n\xec]/'

print('------------------------------------------------------------------------------')
print('------------------------------------------------------------------------------')
print('------------------------------------------------------------------------------')
print('------------------------------------------------------------------------------')
print(os.curdir)
# try:
# Assume we're a sub-module in a package.
from api.views import *
# except ImportError:
# try:
#     # Assume we're a sub-module in a package.
#     from api.views import *
# except ImportError:
#     # Apparently no higher-level package has been imported, fall back to a local import.
#
#     try:
#         # Assume we're a sub-module in a package.
#         from . import views
#     except ImportError:
#         # Apparently no higher-level package has been imported, fall back to a local import.
#         import api.views

# if __name__ == '__main__':
#     app.run()
# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask
#
# app = Flask(__name__)
#
# db_conn = 'postgres+psycopg2://admin:12345678@localhost:5432/bills'
#
# app.config['SQLALCHEMY_DATABASE_URI'] = db_conn
# db = SQLAlchemy(app)
# app.secret_key = b'yhb77sw9_"F4Q8z\n\xec]/'
# from .views import *
