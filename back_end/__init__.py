#Windows = set FLASK_APP=app.py  
#Linux export FLASK_APP=app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

from back_end.config import Config

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)
db.create_all

#Funções para criação de Hash das senhas
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#Cria a moderação para controle de logins
login_mananger = LoginManager(app)
login_mananger.login_view ='usuarios.logar_usuario'
login_mananger.login_message_category = 'info'

mail = Mail(app)

#Importa as rotas dos Blueprints
from back_end.usuarios.routes import usuarios
app.register_blueprint(usuarios)

from back_end.personagens.routes import personagens
app.register_blueprint(personagens)

from back_end.geral.routes import geral
app.register_blueprint(geral)

from back_end.erros.handlers import erros
app.register_blueprint(erros)