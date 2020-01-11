from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, PasswordField, SubmitField, IntegerField, 
                    TextAreaField, BooleanField, ValidationError)
from wtforms.validators import (DataRequired, Length, Email, EqualTo,
                                NumberRange, ValidationError)
from projeto_rpg.models_db import Usuario
from flask_login import current_user

class Mensagem_erro(object):

    def erro_tamanho(self, min_val, max_val):
        return f"O dado deve conter de {str(min_val)} até {str(max_val)} caracteres!"

    def erro_obrigatorio(self):
        return "Esse campo é obrigatório!"

    def erro_entre(self, comeco, final):
        return f"Esse dado deve estar entre {str(comeco)} e {str(final)}"


erros = Mensagem_erro()

# Formulário para o registro de novo usuário
class Form_Registrar_Usuario(FlaskForm):

    nome = StringField('Nome de usuário: ',
                       validators=[DataRequired(),
                                   Length(min=3, max=33)])

    email = StringField('E-mail: ',
                        validators=[DataRequired(),
                                    Email()])

    senha = PasswordField('Senha: ',
                          validators=[DataRequired(),
                                      Length(min=5, max=33)])

    confirmar_senha = PasswordField(' Confirmar a senha: ',
                                    validators=[DataRequired(),
                                                Length(min=5, max=33),
                                                EqualTo('senha')])

    foto = FileField('Editar imagem de perfil: ', validators=[
                     FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])

    botao_registrar = SubmitField('Registrar ')

    #Verificar se já tem algum usuário registrado com o mesmo nome
    def validate_nome(self, nome):
        nome_existente = Usuario.query.filter_by(nome=nome.data).first()
        if nome_existente:
            raise ValidationError('Nome de usuário já registrado! Tente outro')

    #Verificar se já tem algum usuário registrado com o mesmo e-mail
    def validate_email(self, email):
        email_existente = Usuario.query.filter_by(email=email.data).first()
        if email_existente:
            raise ValidationError('Email já registrado! Tente outro')

# Formulário para login de usuário
class Form_Logar_Usuario(FlaskForm):

    nome = StringField('Nome de usuário: ',
                       validators=[DataRequired(),
                                   Length(min=3, max=33)])

    senha = PasswordField('Senha: ',
                          validators=[DataRequired(),
                                      Length(min=5, max=33)])

    permanecer_logado = BooleanField('Permanecer Logado')

    botao_logar = SubmitField('Logar ')


# Formulário para edição dos dados de usuário
class Form_Editar_Conta(FlaskForm):

    nome = StringField('Novo nome de usuário: ',
                       validators=[DataRequired(message=erros.erro_obrigatorio()),
                                   Length(min=3, max=33, message=erros.erro_tamanho(3,33))])

    email = StringField('Novo e-mail: ',
                        validators=[DataRequired(message=erros.erro_obrigatorio()),
                                    Email(message="Informe um endereço de e-mail válido!")])

    imagem_perfil = FileField('Editar imagem de perfil: ', validators=[
                              FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])

    botao_editar = SubmitField('Editar ')

    def validate_nome(self, nome):
        if nome.data != current_user.nome:
            nome_existente = Usuario.query.filter_by(nome=nome.data).first()
            if nome_existente:
                raise ValidationError(
                    'Nome de usuário já registrado! Tente outro')

    def validate_email(self, email):
        if email.data != current_user.email:
            email_existente = Usuario.query.filter_by(email=email.data).first()
            if email_existente:
                raise ValidationError('E-mail já registrado! Tente outro')


# Formulário para informar o e-mail para recuperar senha
class Form_Requisitar_Recuperacao(FlaskForm):

    email = StringField('E-mail da conta: ',
                        validators=[DataRequired(message=erros.erro_obrigatorio()),
                                    Email(message="Informe um endereço de e-mail válido!")])

    botao_requisitar = SubmitField('Requisitar')

    def validate_email(self, email):
        email_existente = Usuario.query.filter_by(email=email.data).first()
        if email_existente is None:
            raise ValidationError('Esse e-mail não esta registrado! Tente outro')

# Formulário para alterar a senha do usuário
class Form_Alterar_Senha(FlaskForm):

    senha = PasswordField('Senha: ',
                          validators=[DataRequired(),
                                      Length(min=5, max=33)])

    confirmar_senha = PasswordField(' Confirmar a senha: ',
                                    validators=[DataRequired(),
                                                Length(min=5, max=33),
                                                EqualTo('senha')])

    botao_enviar = SubmitField('Alterar')

    def validate_email(self, email):
        email_existente = Usuario.query.filter_by(email=email.data).first()
        if email_existente is None:
            raise ValidationError('Esse e-mail não esta registrado! Tente outro')
