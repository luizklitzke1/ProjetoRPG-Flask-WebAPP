from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from projeto_rpg.models_db import Usuario
from flask_login import current_user


#Formulário para o registro de novo usuário
class Form_Registrar_Usuario(FlaskForm):

    nome = StringField('Nome de usuário: ', 
                        validators = [DataRequired(), 
                        Length(min = 3, max = 33)])

    email = StringField('E-mail: ',
                        validators = [DataRequired(), 
                        Email()])

    senha = PasswordField('Senha: ',
                        validators = [DataRequired(), 
                        Length(min = 5, max = 33)])

    confirmar_senha = PasswordField(' Confirmar a senha: ',
                        validators = [DataRequired(), 
                        Length(min = 5, max = 33),
                        EqualTo('senha')])

    foto = FileField('Editar imagem de perfil: ', validators = [FileAllowed(['jpg', 'png', 'gif'])])

    enviar = SubmitField('Registrar ')


    def validate_nome(self, nome):
        nome_existente = Usuario.query.filter_by(nome=nome.data).first()
        if nome_existente:
            raise ValidationError('Nome de usuário já registrado! Tente outro')

    def validate_email(self, email):
        email_existente = Usuario.query.filter_by(email=email.data).first()
        if email_existente:
            raise ValidationError('Email já registrado! Tente outro')

#Formulário para login de usuário
class Form_Logar_Usuario(FlaskForm):

    nome = StringField('Nome de usuário: ', 
                        validators = [DataRequired(), 
                        Length(min = 3, max = 33)])

    senha = PasswordField('Senha: ',
                        validators = [DataRequired(), 
                        Length(min = 5, max = 33)])

    permanecer_logado = BooleanField('Permanecer Logado')

    enviar = SubmitField('Logar ')

#Formulário para edição dos dados de usuário
class Form_Editar_Conta(FlaskForm):
    
    nome = StringField('Novo nome de usuário: ', 
                        validators = [DataRequired(), 
                        Length(min = 3, max = 33)])

    email = StringField('Novo e-mail: ',
                        validators = [DataRequired(), 
                        Email()])

    imagem_perfil = FileField('Editar imagem de perfil: ', validators = [FileAllowed(['jpg', 'png', 'gif'])])

    enviar = SubmitField('Editar ')


    def validate_nome(self, nome):
        if nome.data != current_user.nome:
            nome_existente = Usuario.query.filter_by(nome=nome.data).first()
            if nome_existente:
                raise ValidationError('Nome de usuário já registrado! Tente outro')

    def validate_email(self, email):
        if email.data != current_user.email:
            email_existente = Usuario.query.filter_by(email=email.data).first()
            if email_existente:
                raise ValidationError('Email já registrado! Tente outro')

#Formulário para registro de novo personagem
class Form_Personagem(FlaskForm):

    nome = StringField('Nome: ', 
                        validators = [DataRequired(), 
                        Length(min = 3, max = 33)])

    raca = StringField('Raça: ',
                        validators = [DataRequired(), 
                        Length(min = 3, max = 33)])

    classe = StringField('Classe: ',
                        validators = [DataRequired(), 
                        Length(min = 3, max = 33)])

    nivel = IntegerField('Nível: ', validators = [DataRequired()])

    forca = IntegerField('Força: ', validators = [DataRequired()])

    destreza = IntegerField('Destreza: ', validators = [DataRequired()])

    constituicao = IntegerField('Constituição: ', validators = [DataRequired()])

    inteligencia = IntegerField('Inteligência: ', validators = [DataRequired()])

    sabedoria = IntegerField('Sabedoria: ', validators = [DataRequired()])

    carisma = IntegerField('Carisma: ', validators = [DataRequired()])

    antecedente = TextAreaField('Antecedente: ')

    foto_referencia = FileField('Imagem de referência: ', validators = [FileAllowed(['jpg', 'png', 'gif'])])

    enviar = SubmitField('Registrar ')
