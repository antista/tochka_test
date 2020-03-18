from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db_conn = 'postgres://nuhjrbye:fZ5gd1PqRaBJdx9MUUW0H3KaswyE5_Oi@drona.db.elephantsql.com:5432/nuhjrbye'

app.config['SQLALCHEMY_DATABASE_URI'] = db_conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = b'yhb77sw9_"F4Q8z\n\xec]/'

from api.views import *
