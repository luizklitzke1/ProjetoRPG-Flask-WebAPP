#Windows = set FLASK_APP=app.py  
#Linux export FLASK_APP=app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from datetime import datetime

app = Flask(__name__)

#Chave pra criptografia
app.config['SECRET_KEY'] = 'bd023b5638a8f04016fdedf53a2f3736'

#Caminho e configuração para o Banco de Dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rpg.db'
db = SQLAlchemy(app)

#Funções para criação de Hash das senhas
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#Cria a moderação para controle de logins
login_mananger = LoginManager(app)
login_mananger.login_view ='logar_usuario'
login_mananger.login_message_category = 'info'

#Importa as rotas no final para evitar problemas de import em loop
from projeto_rpg import routes