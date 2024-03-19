from flask import Flask, render_template, request, redirect, session,make_response, jsonify
from flask_session import Session
from flask_mail import Mail, Message
import os
import rotas_public
import rotas_autenticado
import config

app =Flask(__name__)

#configuração da pasta para uploads
config.config_upload(app)

#configuração dos cookies de sessão
config.config_session(app)

#configuração do email
config.config_mail(app)

mail=Mail(app)

#Rotas
rotas_public.setup_public_routes(app,mail)
rotas_autenticado.setup_auth_routes(app)

#erros
@app.errorhandler(404)
def erro_404(evento):
    return render_template("erros/404.html")

app.run(debug=True)