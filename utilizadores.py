from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import basedados
import requests
import bcrypt

RECAPTCHA_SITE_KEY="6LdigYIpAAAAAJGfpZWySe7yuKo61E9GG3pzCEcP"
RECAPTCHA_SECRET_KEY="6LdigYIpAAAAAFp6nHlosWycTpglAC-bbxUe_QyB"

def RegistoUtilizador():
    if request.method=="GET":
        return render_template("utilizadores/registo.html",site_key=RECAPTCHA_SITE_KEY)
    if request.method=="POST":
        ligacao_bd=basedados.criar_conexao("vetonline.bd")
        #verificar o reCAPTCHA
        recaptcha_response = request.form['g-recaptcha-response']
        payload={'response':recaptcha_response,'secret':RECAPTCHA_SECRET_KEY}
        response=requests.post('https://www.google.com/recaptcha/api/siteverify',data=payload)
        response_data=response.json()
        print(response_data)
        if response_data["success"]:
            nome=request.form.get("nome")
            email=request.form.get("email")
            palavra_passe=request.form.get("password")
            if not nome or not email:
                return render_template("utilizadores/registo.html",site_key=RECAPTCHA_SITE_KEY,mensagem="Tem de indicar um nome e um email.")
            #verificar se o email está repetido
            sql="SELECT count(*) as Contar FROM Utilizadores WHERE email=?"
            parametros=(email,)
            dados=basedados.consultar_sql(ligacao_bd,sql,parametros)
            if dados and dados[0]["Contar"]>0:
                return render_template("utilizadores/registo.html",site_key=RECAPTCHA_SITE_KEY,mensagem="Esse email já existe na nossa base de dados.")
            #inserir na bd
            palavra_passe=palavra_passe.encode('utf-8')
            #gerar sal
            sal = bcrypt.gensalt()
            #hash da palavra
            palavra_hash = bcrypt.hashpw(palavra_passe,sal)
            sql = """INSERT INTO Utilizadores(nome,email,password_hash,sal,perfil) VALUES
                        (?,?,?,?,'user')"""
            parametros=(nome,email,palavra_hash,sal)
            basedados.executar_sql(ligacao_bd,sql,parametros)
            #TODO: Redirecionar para ?????
            return "Utilizador registado com sucesso!"
        else:
            return render_template("utilizadores/registo.html",site_key=RECAPTCHA_SITE_KEY,mensagem="Tem de provar que não é um robot.")

#Função para listar todos os utilizadores registados na página listar.html da pasta utilizadores
#Só para admin
def Listar():
    pass

#Só para admin
def Adicionar():
    pass

#Só para admin
def Apagar():
    pass

#Só para admin
def ApagarConfirmado():
    pass

#Só para admin
def Editar():
    pass

#Só para admin
def EditarConfirmado():
    pass