from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from multiprocessing import Pipe

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '7aadefb24fc971006f760dac'
db = SQLAlchemy(app)

pc, cc = Pipe()

from EngineAPI import routes