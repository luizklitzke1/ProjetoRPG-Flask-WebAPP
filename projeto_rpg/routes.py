from flask import render_template, url_for, flash, redirect, request, abort
from PIL import Image
from projeto_rpg.forms import Form_Registrar_Usuario, Form_Logar_Usuario, Form_Editar_Conta, Form_Personagem
from projeto_rpg.models_db import Usuario, Personagem
from projeto_rpg import app, db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os


# Rota para a home
@app.route("/")
@app.route("/home")
def home():
    pagina = request.args.get('pagina', 1, type=int)
    personagens = Personagem.query.order_by(
        Personagem.criacao.desc()).paginate(per_page=3, page=pagina)
    return render_template('home.html', personagens=personagens)


@app.route("/about")
def about():
    return render_template('about.html', titulo='About')

# Rota para registro de usuários novos
@app.route("/registrar_usuario", methods=['GET', 'POST'])
def registrar_usuario():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = Form_Registrar_Usuario()

    if form.validate_on_submit():
        senha_hash = bcrypt.generate_password_hash(
            form.senha.data).decode('utf-8')

        if form.foto.data:
            picture_file = salvar_imagem(
                'static/imagens_perfil', form.foto.data)
            form.foto.data = picture_file

        novo_usuaio = Usuario(
            nome=form.nome.data, email=form.email.data, senha=senha_hash, foto=form.foto.data)
        db.session.add(novo_usuaio)
        db.session.commit()
        flash(f'{form.nome.data} sua conta foi registrada com sucesso!', 'success')
        return redirect(url_for('logar_usuario'))

    else:
        return render_template('registrar_usuario.html', titulo='Registrar Usuário', form=form)

# Rota para login de usuários
@app.route("/logar_usuario", methods=['GET', 'POST'])
def logar_usuario():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = Form_Logar_Usuario()

    if form.validate_on_submit():

        usuario = Usuario.query.filter_by(nome=form.nome.data).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario, remember=form.permanecer_logado.data)
            acessar_pagina = request.args.get('next')
            flash('Login concluído com sucesso', 'success')
            return redirect(acessar_pagina) if acessar_pagina else redirect(url_for('home'))
        else:
            flash('Login falho, por favor verifique os dados informados', 'danger')
    return render_template('logar_usuario.html', titulo='Login', form=form)

# Rota para deslogar usuários
@app.route("/deslogar_usuario")
def deslogar_usuario():
    logout_user()
    flash('Usuário deslogado com sucesso!', 'success')
    return redirect(url_for('home'))


# Método para salvar imagens de perfil compactadas
def salvar_imagem(diretorio, form_picture):
    rhex = secrets.token_hex(9)
    _, foto_ext = os.path.splitext(form_picture.filename)
    print(foto_ext)
    nome_foto = rhex + foto_ext
    caminho = os.path.join(app.root_path, diretorio, nome_foto)

    # Resize na imagem antes de upar, se não for GIF
    if foto_ext != '.gif':
        tamanho_imagem = (150, 150)
        imagem_menor = Image.open(form_picture)
        imagem_menor.thumbnail(tamanho_imagem)
        imagem_menor.save(caminho)
    else:
        form_picture.save(caminho)
    return nome_foto

# Rota para o perfil dos usuários
@app.route("/perfil_usuario/<int:usuario_id>/", methods=['GET', 'POST'])
@login_required
def perfil_usuario(usuario_id):

    form = Form_Editar_Conta()
    pagina = request.args.get('pagina', 1, type=int)
    personagens = Personagem.query.filter_by(
        criador=usuario_id).paginate(per_page=3, page=pagina)
    #personagens = Personagem.query.filter_by(criador=usuario_id)
    usuario = Usuario.query.filter_by(id=usuario_id).first()

    if usuario_id == current_user.id or current_user.isAdmin == True:
        if form.validate_on_submit():

            if form.imagem_perfil.data:
                picture_file = salvar_imagem(
                    'static/imagens_perfil', form.imagem_perfil.data)
                current_user.foto = picture_file

            current_user.nome = form.nome.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Conta atualizada com sucesso!', 'success')
            return redirect(url_for('perfil_usuario',  usuario_id=usuario_id, personagens=personagens))

        elif request.method == "GET":
            form.nome.data = usuario.nome
            form.email.data = usuario.email
        imagem_perfil = url_for(
            'static', filename='imagens_perfil/' + current_user.foto)

    return render_template('perfil_usuario.html', usuario=usuario, personagens=personagens, form=form)

# Rota para registrar personagens
@app.route("/registrar_personagem", methods=['GET', 'POST'])
@login_required
def registrar_personagem():
    form = Form_Personagem()

    if form.validate_on_submit():

        if form.foto_referencia.data:
            picture_file = salvar_imagem(
                'static/imagens_personagens', form.foto_referencia.data)
            form.foto_referencia.data = picture_file

        novo_personagem = Personagem(nome=form.nome.data, raca=form.raca.data,
                                     classe=form.classe.data, nivel=form.nivel.data,
                                     forca=form.forca.data, destreza=form.destreza.data,
                                     constituicao=form.constituicao.data, inteligencia=form.inteligencia.data,
                                     sabedoria=form.sabedoria.data, carisma=form.carisma.data,
                                     antecedente=form.antecedente.data, foto=form.foto_referencia.data,
                                     autor=current_user)

        db.session.add(novo_personagem)
        db.session.commit()
        flash('Personagem registrado com sucesso!', 'success')
        return redirect(url_for('home'))

    return render_template('registrar_personagem.html', titulo='Registrar Personagem', form=form)

# Rota para vizualizar um personagem
@app.route("/personagem/<int:personagem_id>")
def ver_personagem(personagem_id):
    personagem = Personagem.query.get_or_404(personagem_id)
    return render_template('personagem.html', titulo='personagem.nome', personagem=personagem)

# Rota para editar um personagem
@app.route("/personagem/<int:personagem_id>/editar",  methods=['GET', 'POST'])
@login_required
def editar_personagem(personagem_id):

    personagem = Personagem.query.get_or_404(personagem_id)

    if (personagem.autor != current_user) and not(current_user.isAdmin):
        abort(403)

    form = Form_Personagem()

    if form.validate_on_submit():

        personagem.nome = form.nome.data
        personagem.raca = form.raca.data
        personagem.classe = form.classe.data
        personagem.nivel = form.nivel.data
        personagem.forca = form.forca.data
        personagem.destreza = form.destreza.data
        personagem.constituicao = form.constituicao.data
        personagem.inteligencia = form.inteligencia.data
        personagem.sabedoria = form.sabedoria.data
        personagem.carisma = form.carisma.data

        personagem.antecedente = form.antecedente.data

        if form.foto_referencia.data:
            picture_file = salvar_imagem(
                'static/imagens_personagens', form.foto_referencia.data)
            personagem.foto = picture_file

        db.session.commit()
        flash('Personagem editado com sucesso!', 'success')
        return redirect(url_for('ver_personagem', personagem_id=personagem.id))

    elif request.method == "GET":
        form.nome.data = personagem.nome
        form.raca.data = personagem.raca
        form.classe.data = personagem.classe
        form.nivel.data = personagem.nivel
        form.forca.data = personagem.forca
        form.destreza.data = personagem.destreza
        form.constituicao.data = personagem.constituicao
        form.inteligencia.data = personagem.inteligencia
        form.sabedoria.data = personagem.sabedoria
        form.carisma.data = personagem.carisma
        form.antecedente.data = personagem.antecedente

    return render_template('editar_personagem.html', titulo='personagem.nome', form=form, personagem=personagem)

# Rota para apagar um personagem
@app.route("/personagem/<int:personagem_id>/apagar",  methods=['POST'])
@login_required
def apagar_personagem(personagem_id):
    personagem = Personagem.query.get_or_404(personagem_id)
    if (personagem.autor != current_user) and not(current_user.isAdmin):
        abort(403)
    db.session.delete(personagem)
    db.session.commit()
    flash('Personagem apagado com sucesso!', 'success')
    return redirect(url_for('home'))
