
from flask import Blueprint, jsonify

#Definição da Blueprint
personagens = Blueprint('personagens',__name__)

from flask import render_template, url_for, flash, redirect, request, abort
from back_end.personagens.forms import (Form_Personagem, Form_Procurar_Personagem, 
                                           Form_Avaliar_Personagem)
from back_end.models_db import Personagem, Avaliacao, Usuario
from back_end import app, db
from flask_login import current_user, login_required
from back_end.geral.routes import salvar_imagem, apagar_imagem
from datetime import datetime

# Rota para registrar personagens
@personagens.route("/registrar_personagem", methods=['GET', 'POST'])
@login_required
def registrar_personagem():
    
    form_personagem = Form_Personagem()

    if form_personagem.validate_on_submit():

        if form_personagem.foto_referencia.data:
            picture_file = salvar_imagem(
                'static/imagens_personagens', form_personagem.foto_referencia.data)
            form_personagem.foto_referencia.data = picture_file

        novo_personagem = Personagem(nome=form_personagem.nome.data, 
                                     raca=form_personagem.raca.data,
                                     classe=form_personagem.classe.data, 
                                     nivel=form_personagem.nivel.data,
                                     forca=form_personagem.forca.data, 
                                     destreza=form_personagem.destreza.data,
                                     constituicao=form_personagem.constituicao.data, 
                                     inteligencia=form_personagem.inteligencia.data,
                                     sabedoria=form_personagem.sabedoria.data, 
                                     carisma=form_personagem.carisma.data,
                                     historia=form_personagem.historia.data, 
                                     foto=form_personagem.foto_referencia.data,
                                     autor=current_user)

        db.session.add(novo_personagem)
        db.session.commit()
        flash('Personagem registrado com sucesso!', 'success')
        return redirect(url_for('geral.mostrar_home'))

    return render_template('registrar_personagem.html', titulo='Registrar Personagem', 
                            form_personagem=form_personagem)

# Rota para vizualizar um personagem
@personagens.route("/personagem/<int:personagem_id>", methods=['GET', 'POST'])
def mostrar_personagem(personagem_id):

    pagina = request.args.get('pagina', 1, type=int)

    personagem = Personagem.query.get_or_404(personagem_id)


    if current_user.is_authenticated:
        #Pega todas as avaliações, fora a do usuário atual
        avaliacoes = Avaliacao.query.filter(Avaliacao.autor_id.isnot(current_user.id),
                    Avaliacao.personagem_id.is_(personagem_id)).paginate(page=pagina, per_page=6)
        #Verificar se o usuáriojá possui alguma avaliação para ser editada
        avaliacao_usuario = Avaliacao.query.filter_by(autor_id=current_user.id, 
                                                         personagem_id = personagem_id).first()
    else:
        avaliacao_usuario = None

    #Pega todas as avaliações
        avaliacoes = Avaliacao.query.filter_by(personagem_id = personagem_id).paginate(page=pagina, per_page=6)

    #Atualiza a nota do personagem
    lista_notas = []
    nota = 0
    for avaliacao in avaliacoes.items:
        lista_notas.append(avaliacao.nota)
        nota += avaliacao.nota
    if avaliacao_usuario:
        lista_notas.append(avaliacao_usuario.nota)
        nota += avaliacao_usuario.nota

    if len(lista_notas) == 0:
        personagem.nota = None
    else:
        personagem.nota = round((nota/len(lista_notas)),2) 

    db.session.commit()

    form_avaliar = Form_Avaliar_Personagem()
    form_editar_avaliacao = Form_Avaliar_Personagem()

    #Verifica se uma avaliação foi editada
    if avaliacao_usuario and form_editar_avaliacao.validate_on_submit():

        avaliacao_usuario.data_postagem = datetime.now()

        avaliacao_usuario.conteudo = form_editar_avaliacao.conteudo.data

        avaliacao_usuario.nota = form_editar_avaliacao.nota.data

        db.session.commit()
        flash('Avaliação editada com sucesso!', 'success')
        return redirect(url_for('personagens.mostrar_personagem', personagem_id=personagem.id))

    #Verifica se uma nova avaliação foi registrada
    elif form_avaliar.validate_on_submit():

        nova_avalicao = Avaliacao(autor_id = current_user.id, personagem_id = personagem_id, 
                                  conteudo = form_avaliar.conteudo.data, nota = form_avaliar.nota.data)


        db.session.add(nova_avalicao)
        db.session.commit()

        flash('Personagem avaliado com sucesso!', 'success')
        return redirect(url_for('personagens.mostrar_personagem', personagem_id=personagem.id))

    #Pré-popula os campos da avaliação caso for ser editada
    elif request.method == "GET" and avaliacao_usuario:

        form_editar_avaliacao.nota.data = avaliacao_usuario.nota 
        form_editar_avaliacao.conteudo.data = avaliacao_usuario.conteudo
        
    return render_template('personagem.html', titulo=personagem.nome,  personagem = personagem,
                                              avaliacoes = avaliacoes, form_avaliar = form_avaliar, 
                                              form_editar_avaliacao = form_editar_avaliacao,
                                              avaliacao_usuario = avaliacao_usuario )

# Rota para apagar um personagem
@personagens.route("/personagem/<int:personagem_id>/apagar_avaliacao/<int:autor_id>",  methods=['POST', 'GET'])
@login_required
def apagar_avaliacao(personagem_id, autor_id):

    avaliacao = Avaliacao.query.get_or_404 ((autor_id, personagem_id))
    avaliacoes = Avaliacao.query.filter_by(personagem_id = personagem_id)

    personagem = Personagem.query.get_or_404 (personagem_id)

    if (avaliacao.autor != current_user) and not(current_user.isAdmin):
        abort(403)

    #Verifica se é a única avaliação do personagem
    #(Caso for, considera ele ainda não avaliado)
    if avaliacoes.count() == 1:
        personagem.nota = None
    else:
        #Caso não for, remove a nota da média do personagem
        personagem.nota = ((personagem.nota)*2) - avaliacao.nota
    
    db.session.delete(avaliacao)
    db.session.commit()
    flash('Avaliação apagada com sucesso!', 'success')
    return redirect(url_for('personagens.mostrar_personagem', personagem_id=personagem_id))


# Rota para editar um personagem
@personagens.route("/personagem/<int:personagem_id>/editar",  methods=['GET', 'POST'])
@login_required
def editar_personagem(personagem_id):
    
    print("aaaaaaaaaaaaa")

    personagem = Personagem.query.get_or_404(personagem_id)

    if (personagem.autor != current_user) and not(current_user.isAdmin):
        abort(403)

    form_editar = Form_Personagem()

    if form_editar.validate_on_submit():

        personagem.nome = form_editar.nome.data
        personagem.raca = form_editar.raca.data
        personagem.classe = form_editar.classe.data
        personagem.nivel = form_editar.nivel.data
        personagem.forca = form_editar.forca.data
        personagem.destreza = form_editar.destreza.data
        personagem.constituicao = form_editar.constituicao.data
        personagem.inteligencia = form_editar.inteligencia.data
        personagem.sabedoria = form_editar.sabedoria.data
        personagem.carisma = form_editar.carisma.data
        personagem.historia = form_editar.historia.data

        if form_editar.foto_referencia.data:
            if personagem.foto != 'personagem.png':
                apagar_imagem('static/imagens_personagens', personagem.foto)
            picture_file = salvar_imagem('static/imagens_personagens', form_editar.foto_referencia.data)
            personagem.foto = picture_file

        db.session.commit()
        flash('Personagem editado com sucesso!', 'success')
        return redirect(url_for('personagens.mostrar_personagem', personagem_id=personagem.id))

    elif request.method == "GET":
        
        #Pré-popular os campos com os dados do personagem 
        form_editar = Form_Personagem(personagem.nome, personagem.raca, personagem.classe, personagem.nivel,
                               personagem.forca, personagem.destreza, personagem.constituicao,
                               personagem.inteligencia, personagem.sabedoria, personagem.carisma, 
                               personagem.historia)


    return render_template('editar_personagem.html', titulo='personagem.nome', form_editar=form_editar, 
                                                     personagem=personagem)

# Rota para apagar um personagem
@personagens.route("/personagem/<int:personagem_id>/apagar",  methods=['POST'])
@login_required
def apagar_personagem(personagem_id):
    personagem = Personagem.query.get_or_404(personagem_id)
    if (personagem.autor != current_user) and not(current_user.isAdmin):
        abort(403)

    #Apagar as avaliações do personagem
    #(Não sei porque não apaga automaticamente na verdade)
    avaliacoes = Avaliacao.query.filter_by(personagem_id = personagem_id)
    for avaliacao in avaliacoes:
        db.session.delete(avaliacao)
        
    if personagem.foto != 'personagem.png':
                apagar_imagem('static/imagens_personagens', personagem.foto)
    db.session.delete(personagem)
    db.session.commit()
    flash('Personagem apagado com sucesso!', 'success')
    return redirect(url_for('geral.mostrar_home'))


# Rota para a pesquisa de personagem
@personagens.route("/procurar_personagem/", methods=['GET', 'POST'])
def procurar_personagem():
    
    print("aaaaaaaaa")
    pagina = request.args.get('pagina', 1, type=int)   

    form_procurar_pers = Form_Procurar_Personagem()
    pagina = request.args.get('pagina', 1, type=int)

    #Se tiverem sido informados dados para o filtro
    if form_procurar_pers.validate_on_submit():

        personagens = db.session.query(Personagem).filter(
                                                          Personagem.nome.like(f"%{form_procurar_pers.nome.data}%"),
                                                          Personagem.raca.like(f"%{form_procurar_pers.raca.data}%"),
                                                          Personagem.classe.like(f"%{form_procurar_pers.classe.data}%"),
                                                          ).from_self().paginate(page=1, per_page=9).items
    #Se nenhum filtro for informado:
    else:
        personagens = db.session.query(Personagem).filter(Personagem.nome.like('%%')).from_self().paginate(page=pagina, 
                                                                                                           per_page=9).items
    personagens_json = [personagem.json() for personagem in personagens]
    return jsonify(personagens_json)

    
    #return render_template('procurar_personagem.html', titulo='Procurar Personagem', 
    #                        form_procurar_pers = form_procurar_pers, personagens = personagens)
