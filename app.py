from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import basedados
import tabelas
import utilizadores

app =Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/Utilizadores/registo',methods=["POST","GET"])
def Registo():
    return utilizadores.RegistoUtilizador()

app.run(debug=True)