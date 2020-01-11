from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, PasswordField, SubmitField, IntegerField, TextAreaField, 
                    BooleanField,ValidationError, FloatField)
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from flask_login import current_user

class Mensagem_erro(object):

    def erro_tamanho(self, min_val, max_val):
        return f"O dado deve conter de {str(min_val)} até {str(max_val)} caracteres!"

    def erro_obrigatorio(self):
        return "Esse campo é obrigatório!"

    def erro_entre(self, comeco, final):
        return f"Esse dado deve estar entre {str(comeco)} e {str(final)}"


erros = Mensagem_erro()

# Formulário para registro de novo personagem
class Form_Personagem(FlaskForm):

    nome = StringField('Nome:',
                       validators=[DataRequired(message=erros.erro_obrigatorio()),
                                   Length(min=3, max=33, 
                                   message=erros.erro_tamanho(3,33),)])

    raca = StringField('Raça:',
                       validators=[DataRequired(message=erros.erro_obrigatorio()),
                                   Length(min=3, max=33, 
                                   message=erros.erro_tamanho(3,33))])

    classe = StringField('Classe:',
                       validators=[DataRequired(message=erros.erro_obrigatorio()),
                                   Length(min=3, max=33, 
                                   message=erros.erro_tamanho(3,33))])

    nivel = IntegerField('Nível:', validators=[DataRequired(message=erros.erro_obrigatorio()), 
                                                NumberRange(min=-12, max=99, 
                                                message=erros.erro_entre(1,99))])

    forca = IntegerField('Força:', validators=[DataRequired(message=erros.erro_obrigatorio()), 
                                                NumberRange(min=0, max=99, 
                                                message=erros.erro_entre(1,99))])

    destreza = IntegerField('Destreza:', validators=[DataRequired(message=erros.erro_obrigatorio()), 
                                                      NumberRange(min=0, max=99, 
                                                      message=erros.erro_entre(1,99))])

    constituicao = IntegerField('Constituição:', validators=[DataRequired(message=erros.erro_obrigatorio()), 
                                                              NumberRange(min=0, max=99, 
                                                              message=erros.erro_entre(1,99))])

    inteligencia = IntegerField('Inteligência:', validators=[DataRequired(message=erros.erro_obrigatorio()), 
                                                              NumberRange(min=0, max=99, 
                                                              message=erros.erro_entre(1,99))])

    sabedoria = IntegerField('Sabedoria:', validators=[DataRequired(message=erros.erro_obrigatorio()),
                                                        NumberRange(min=0, max=99, 
                                                        message=erros.erro_entre(1,99))])

    carisma = IntegerField('Carisma:', validators=[DataRequired(message=erros.erro_obrigatorio()), 
                                                    NumberRange(min=0, max=99, 
                                                    message=erros.erro_entre(1,99))])

    historia = TextAreaField('História:')

    foto_referencia = FileField('Imagem de referência: ', validators=[
                                FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])


    #Nome genérico, o value é dado dependendo se vair registrar novo ou editar
    botao_enviar = SubmitField('Enviar ')


    #Passar os valores no __init__ para pré-popular os campos caso for editar
    def __init__(self, nome2=None,raca2=None,classe2=None,nivel2=None,forca2=None,
                destreza2=None,constituicao2=None,inteligencia2=None,
                sabedoria2=None,carisma2=None,historia2=None, *args, **kwargs):
        
        super().__init__(*args, **kwargs)

        #Testa se o primeiro dado existe
        #Fiz isso porque se deixasse assim, os valores passavam como NULL
        #E dava erro na hora de registrar um personagem

        if nome2:
            self.nome.data = nome2
            self.raca.data = raca2
            self.classe.data = classe2
            self.nivel.data = nivel2
            self.forca.data = forca2
            self.destreza.data = destreza2
            self.constituicao.data = constituicao2
            self.inteligencia.data = inteligencia2
            self.sabedoria.data = sabedoria2
            self.carisma.data = carisma2
            self.historia.data = historia2

# Formulário para procurar por um personagem
class Form_Procurar_Personagem(FlaskForm):

    nome = StringField('Nome: ')

    raca = StringField('Raça: ')

    classe = StringField('Classe: ')

    autor = StringField('Autor: ')

    botao_procurar = SubmitField('Procurar ')


# Formulário para avaliacão de personagem
class Form_Avaliar_Personagem(FlaskForm):

    nota = FloatField('Deixe uma nota: ', validators=[DataRequired(message=erros.erro_obrigatorio()), 
                                                     NumberRange(min=0, max =5 , message=erros.erro_entre(0,5))])
    
    conteudo = TextAreaField('Deixe sua avaliação: ', validators=[DataRequired(message=erros.erro_obrigatorio())])

    botao_avaliar = SubmitField('Avaliar ')

