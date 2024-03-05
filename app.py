from flask import Flask, render_template, request, redirect, session,make_response
from flask_session import Session
import basedados
import tabelas
import utilizadores
import animais
import os

app =Flask(__name__)

UPLOAD_FOLDER=os.path.join(app.root_path,"static/imagens")
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

@app.route('/aceitar_cookies',methods=['POST'])
def aceitar_cookies():
    resposta = make_response(redirect("/"))
    #cookie com prazo de validade de 30 dias
    resposta.set_cookie('avisoM06','aceitou',max_age=30*24*60*60)
    return resposta

#Rotas public
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/Utilizadores/registo',methods=["POST","GET"])
def Registo():
    return utilizadores.RegistoUtilizador()

#Rotas para user logado

#Rotas para user admin
@app.route("/Animais/adicionar",methods=["POST","GET"])
def AnimaisAdicionar():
    return animais.Adicionar(app)

@app.route("/Animais/listar")
def AnimaisListar():
    return animais.Listar(app)

#erros


app.run(debug=True)