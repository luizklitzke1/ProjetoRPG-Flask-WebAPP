
from flask import Blueprint

geral = Blueprint('geral',__name__)

from flask import render_template
from PIL import Image
from back_end.models_db import Personagem
from back_end import app, db
import secrets
import os

# Rota para a home
@geral.route("/")
@geral.route("/home")
def mostrar_home():

    personagens = Personagem.query.order_by(Personagem.data_criacao.desc()).limit(6)
    return render_template('home.html', personagens=personagens, titulo="Home")

# Método para salvar imagens de perfil compactadas
def salvar_imagem(diretorio, form_picture):
    rhex = secrets.token_hex(9)
    _, foto_ext = os.path.splitext(form_picture.filename)
    print(foto_ext)
    nome_foto = rhex + foto_ext
    caminho = os.path.join(app.root_path, diretorio, nome_foto)

    # Resize na imagem antes de upar, se não for GIF
    if foto_ext != '.gif':
        tamanho_imagem = (200, 200)
        imagem_menor = Image.open(form_picture)
        imagem_menor.thumbnail(tamanho_imagem)
        imagem_menor.save(caminho)
    else:
        form_picture.save(caminho)
    return nome_foto

# Método para apagar as imagens ao apagar um usuário ou personagem
def apagar_imagem(diretorio, foto):
    caminho = os.path.join(app.root_path, diretorio, foto)
    os.remove(caminho)