from datetime import datetime
from projeto_rpg import db, login_mananger, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# Método que mostra como encontrar o id de um usuário
@login_mananger.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


# Modelo para usuários
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(33), unique=True, nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False)
    senha = db.Column(db.String(60), nullable=False)
    data_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)
    
    foto = db.Column(db.String(20), nullable=False, default='usuario.png')

    personagens = db.relationship('Personagem', backref='autor', lazy=True)

    avaliacoes = db.relationship('Avaliacao', backref='autor', lazy=True)

    #Representação em String
    def __repr__(self):
        return f"Nome: '{self.nome}', E-Mail: '{self.email}', Senha: '{self.senha}' "

    #Expressão da classe em Json
    def json(self):
        return {
            "id": self.id, "nome": self.nome,
            "email": self.email, "senha": self.senha,
            "data_registro": self.data_registro,
            "isAdmin": self.isAdmin,
            "foto": self.foto,
            "personagens": self.personagens,
            "avaliacoes": self.avaliacoes
        }
    #Token para a redefinição de senha
    def get_reset_token(self,expirar_segundos=1800):
        s = Serializer(app.config['SECRET_KEY'], expirar_segundos)
        return s.dumps({'usuario_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            usuariod_id = s.loads(token)['usuario_id']
        except:
            return None
        return Usuario.query.get(usuariod_id)


# Modelo para personagens
class Personagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    raca = db.Column(db.String(33), nullable=False)
    classe = db.Column(db.String(33), nullable=False)
    nivel = db.Column(db.Integer, nullable=False)
    forca = db.Column(db.Integer, nullable=False)
    destreza = db.Column(db.Integer, nullable=False)
    constituicao = db.Column(db.Integer, nullable=False)
    inteligencia = db.Column(db.Integer, nullable=False)
    sabedoria = db.Column(db.Integer, nullable=False)
    carisma = db.Column(db.Integer, nullable=False)
    historia = db.Column(db.Text, nullable=False, default='Nenhuma história informada.')
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    foto = db.Column(db.String(20), nullable=False, default='personagem.png')

    nota = db.Column(db.Float, nullable = True)

    criador = db.Column(db.Integer, nullable=False)
    criador = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    #Representação em String
    def __repr__(self):
        return f"Nome: '{self.nome}', Raca: '{self.raca}', Classe: '{self.classe}', Nivel: '{self.nivel}'"

    #Expressão da classe em Json
    def json(self):
        return{
            "id": self.id, "nome": self.nome,
            "raca": self.raca, "classe":self.classe,
            "nivel": self.nivel, "forca": self.forca,
            "destreza": self.destreza, "constituicao": self.constituicao,
            "inteligencia": self.inteligencia, "sabedoria": self.sabedoria,
            "carisma": self.carisma, "historia": self.historia,
            "data_criacao": self.data_criacao, "foto": self.foto,
            "nota": self.nota, "criador": self.criador
            
        }
        
# Modelo para as avaliações
class Avaliacao(db.Model):
    autor_id=db.Column(db.Integer,db.ForeignKey('usuario.id'), primary_key=True)
    personagem_id = db.Column(db.Integer,db.ForeignKey('personagem.id'), primary_key=True)
    conteudo = db.Column(db.Text, nullable = False)
    nota = db.Column(db.Float, nullable = False)
    data_postagem = db.Column(db.DateTime, nullable=False, default=datetime.now)
    

    #Representação em String
    def __repr__(self):
        return f"Personagem_id: '{self.personagem_id}', Autor_id: '{self.autor_id}', Nota:  '{self.nota}', Conteudo: '{self.conteudo}' )"
    
    #Expressão da classe em Json
    def json(self):
        return{
            "autor_id": self.autor_id, "personagem_id": self.personagem_id,
            "conteudo": self.conteudo, "nota": self.nota,
            "data_postagem": self.data_postagem
        }