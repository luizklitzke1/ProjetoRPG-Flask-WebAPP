from flask import Blueprint

usuarios = Blueprint('usuarios',__name__)

from flask import render_template, url_for, flash, redirect, request, abort
from projeto_rpg.usuarios.forms import (Form_Registrar_Usuario, Form_Logar_Usuario, Form_Editar_Conta,
                                        Form_Requisitar_Recuperacao, Form_Alterar_Senha)
from projeto_rpg.models_db import Usuario, Personagem
from projeto_rpg import app, db, bcrypt, mail
from flask_login import login_user, logout_user, current_user, login_required
from projeto_rpg.geral.routes import salvar_imagem, apagar_imagem
from flask_mail import Message

# Rota para registro de usuários novos
@usuarios.route("/registrar_usuario", methods=['GET', 'POST'])
def registrar_usuario():

    if current_user.is_authenticated:
        return redirect(url_for('geral.mostrar_home'))

    form_registrar_usuario = Form_Registrar_Usuario()

    if form_registrar_usuario.validate_on_submit():

        senha_hash = bcrypt.generate_password_hash(
            form_registrar_usuario.senha.data).decode('utf-8')

        if form_registrar_usuario.foto.data:
            picture_file = salvar_imagem('static/imagens_perfil', form_registrar_usuario.foto.data)
            form_registrar_usuario.foto.data = picture_file

        novo_usuaio = Usuario(nome=form_registrar_usuario.nome.data, email=form_registrar_usuario.email.data,
                              senha=senha_hash, foto=form_registrar_usuario.foto.data)
        db.session.add(novo_usuaio)
        db.session.commit()
        flash(f'{form_registrar_usuario.nome.data} sua conta foi registrada com sucesso!', 'success')
        return redirect(url_for('usuarios.logar_usuario'))

    else:
        return render_template('registrar_usuario.html', titulo='Registrar Usuário', form_registrar_usuario=form_registrar_usuario)

# Rota para login de usuários
@usuarios.route("/logar_usuario", methods=['GET', 'POST'])
def logar_usuario():

    if current_user.is_authenticated:
        return redirect(url_for('geral.mostrar_home'))

    form_logar_usuario = Form_Logar_Usuario()

    if form_logar_usuario.validate_on_submit():

        usuario = Usuario.query.filter_by(nome=form_logar_usuario.nome.data).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, form_logar_usuario.senha.data):
            login_user(usuario, remember=form_logar_usuario.permanecer_logado.data)
            acessar_pagina = request.args.get('next')
            flash('Login concluído com sucesso', 'success')
            return redirect(acessar_pagina) if acessar_pagina else redirect(url_for('geral.mostrar_home'))
        else:
            flash('Login falho, por favor verifique os dados informados', 'danger')
    return render_template('logar_usuario.html', titulo='Login', form_logar_usuario=form_logar_usuario)

# Rota para deslogar usuários
@usuarios.route("/deslogar_usuario")
def deslogar_usuario():
    logout_user()
    flash('Usuário deslogado com sucesso!', 'success')
    return redirect(url_for('geral.mostrar_home'))

# Rota para o perfil dos usuários
@usuarios.route("/perfil_usuario/<int:usuario_id>", methods=['GET', 'POST'])
@login_required
def mostrar_perfil_usuario(usuario_id):

    form_editar_conta = Form_Editar_Conta()
    pagina = request.args.get('pagina', 1, type=int)
    personagens = Personagem.query.filter_by(
        criador=usuario_id).paginate(page=pagina, per_page=6)
    usuario = Usuario.query.filter_by(id=usuario_id).first()

    if usuario_id == current_user.id:

        if form_editar_conta.validate_on_submit():

            if form_editar_conta.imagem_perfil.data:

                apagar_imagem('static/imagens_perfil', usuario.foto)
                picture_file = salvar_imagem(
                    'static/imagens_perfil', form_editar_conta.imagem_perfil.data)
                usuario.foto = picture_file

            usuario.nome = form_editar_conta.nome.data
            usuario.email = form_editar_conta.email.data
            db.session.commit()
            flash('Conta atualizada com sucesso!', 'success')
            return redirect(url_for('usuarios.mostrar_perfil_usuario', usuario_id=usuario_id, personagens=personagens,
                                                              titulo = usuario.nome))

        elif request.method == "GET":
            form_editar_conta.nome.data = usuario.nome
            form_editar_conta.email.data = usuario.email
        imagem_perfil = url_for('static', filename='imagens_perfil/' + current_user.foto)

    return render_template('perfil_usuario.html', usuario=usuario, personagens=personagens, form_editar_conta=form_editar_conta, 
                                                  titulo = usuario.nome)

# Rota para apagar um usuário
@usuarios.route("/usuario/<int:usuario_id>/apagar",  methods=['POST'])
@login_required
def apagar_usuario(usuario_id):

    usuario = Usuario.query.get_or_404(usuario_id)

    personagens = Personagem.query.filter_by(criador=usuario_id)

    if usuario.foto != "usuario.png":
        apagar_imagem('static/imagens_perfil', usuario.foto)

    for personagem in personagens:
        if personagem.foto != "personagem.png":
            apagar_imagem('static/imagens_personagens', personagem.foto)
        db.session.delete(personagem)
        db.session.commit()

    db.session.delete(usuario)
    db.session.commit()
    flash('Uusuário apagado com sucesso!', 'success')
    return redirect(url_for('geral.mostrar_home'))


# Rota para enviar o e-mail de recuperação de senha
def enviar_email_recuperacao(usuario):
    token = usuario.get_reset_token()
    msg = Message('Requisição de mudança de senha.', 
                   sender = 'projeto.rpg.suporte@gmail.com', 
                   recipients=[usuario.email])
    msg.body = f'''Para reiniciar sua senha, use o link:
{url_for('recuperar_conta', token = token, _external = True)}
Se não foi você que requisitou esse e-mail, apenas ignore-o.
    '''
    mail.send(msg)


# Rota para requisitar a recuperação de senha
@app.route("/requisitar_recuperacao", methods=['GET', 'POST'])
def requisitar_recuperacao():

    form_requisitar = Form_Requisitar_Recuperacao()

    if form_requisitar.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_requisitar.email.data).first()
        enviar_email_recuperacao(usuario)
        flash('Um e-mail foi enviado com instruções para a recuperação de senha!', 'info')
        return redirect(url_for('usuarios.logar_usuario'))
    return render_template('requisitar_recuperacao.html', titulo='Requisitar Recuperação', 
                                                          form = form_requisitar)

# Rota para requisitar a recuperação de senha
@app.route("/recuperar_conta/<token>", methods=['GET', 'POST'])
def recuperar_conta(token):

    usuario = Usuario.verify_reset_token(token)

    if not usuario:
        flash('O token informado é inválido ou está expirado!', 'warning')
        return redirect(url_for('usuarios.requisitar_recuperacao'))

    form_alterar_senha = Form_Alterar_Senha()

    if form_alterar_senha.validate_on_submit():

        senha_hash = bcrypt.generate_password_hash(
            form_alterar_senha.senha.data).decode('utf-8')

        usuario.senha = senha_hash

        db.session.commit()

        if current_user.is_authenticated:
            logout_user()

        flash(f'{usuario.nome} sua senha foi alterada com sucesso!', 'success')
        return redirect(url_for('usuarios.logar_usuario'))
    return render_template('alterar_senha.html', titulo='Alterar senha', form = form_alterar_senha)