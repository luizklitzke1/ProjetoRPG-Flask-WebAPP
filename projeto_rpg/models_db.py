from datetime import datetime
from projeto_rpg import db, login_mananger
from flask_login import UserMixin


#from projeto_rpg import db
#db.create_all()

#from projeto_rpg.models_db import Usuario
#u = Usuario.query.all()

#Método que mostra como encontrar o id de um usuário
@login_mananger.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


#Modelo para usuários
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(33), unique = True, nullable = False)
    email = db.Column(db.String(180), unique = True, nullable = False)
    senha = db.Column(db.String(60), nullable=False)
    registro = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    isAdmin = db.Column(db.Boolean, nullable = False, default = False)
    foto = db.Column(db.String(20), nullable = False, default='usuario.png')
    
    personagens = db.relationship('Personagem', backref='autor', lazy = True)

    def __repr__(self):
        return f"Nome: '{self.nome}', E-Mail: '{self.email}', Senha: '{self.senha}' "

#Modelo para personagens
class Personagem(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(150), unique = True, nullable = False)
    raca = db.Column(db.String(33), nullable = False)
    classe = db.Column(db.String(33), nullable = False) 
    nivel = db.Column(db.Integer, nullable = False)
    forca = db.Column(db.Integer, nullable = False)
    destreza = db.Column(db.Integer, nullable = False)
    constituicao = db.Column(db.Integer, nullable = False)
    inteligencia = db.Column(db.Integer, nullable = False)
    sabedoria = db.Column(db.Integer, nullable = False)
    carisma = db.Column(db.Integer, nullable = False)
    antecedente =  db.Column(db.Integer, nullable = False, default = 'Nenhum antecedente informado.')
    criacao = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    foto = db.Column(db.String(20), nullable = False, default='personagem.jpg')
    criador = db.Column(db.Integer, nullable = False)

    criador = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable = False)
