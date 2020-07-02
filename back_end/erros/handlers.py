from flask import Blueprint, render_template

erros = Blueprint('erros', __name__)

@erros.app_errorhandler(403)
def erro_404(error):
    return render_template('erros/erro_403.html'), 403

@erros.app_errorhandler(404)
def erro_404(error):
    return render_template('erros/erro_404.html'), 404

@erros.app_errorhandler(500)
def erro_404(error):
    return render_template('erros/erro_500.html'), 500



