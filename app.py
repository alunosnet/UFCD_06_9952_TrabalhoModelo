from flask import Flask, render_template, request, redirect, session,make_response, jsonify
from flask_session import Session
import basedados
import tabelas
import utilizadores
import animais
import consultas
import os

app =Flask(__name__)

#configuração da pasta para uploads
UPLOAD_FOLDER=os.path.join(app.root_path,"static/imagens")
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

#configuração dos cookies de sessão
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)

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

@app.route('/Login',methods=["POST"])
def Login():
    return utilizadores.Login()

#serviço web para devolver a lista dos animais de um utilizador
@app.route('/get_animais',methods=['GET'])
def get_animais():
    id_utilizador=request.args.get('id_utilizador')
    ligacao_bd=basedados.criar_conexao("vetonline.bd")
    if id_utilizador:
        parametros=(id_utilizador,)
        dados=basedados.consultar_sql(ligacao_bd,"SELECT id,nome FROM Animais WHERE id_utilizador=? ORDER BY nome",parametros)
        #converter os dados em uma lista
        dados=[list(animal) for animal in dados]
        return jsonify(dados)
    return jsonify([])

#Rotas para user logado
@app.route("/Consultas/listar",methods=['GET'])
def ConsultasListar():
    if utilizadores.Logado():
        return consultas.Listar()
    return redirect("/")

@app.route('/Logout')
def Logout():
    return utilizadores.Logout()

def EditarPerfil():
    pass
@app.route("/Consultas/marcar",methods=["POST","GET"])
def MarcarConsulta():
    if utilizadores.Logado():
        if utilizadores.Utilizador_E_Admin():
            return consultas.marcar("Confirmada")
        else:
            return consultas.marcar("Pedida")
    return redirect("/")

#Rotas para user admin
@app.route("/Animais/adicionar",methods=["POST","GET"])
def AnimaisAdicionar():
    return animais.Adicionar(app)

@app.route("/Animais/listar")
def AnimaisListar():
    return animais.Listar(app)

def UtilizadorAdicionar():
    pass

def UtilizadorListar():
    pass

def UtilizadorBloquear():
    pass

def UtilizadorEditar():
    pass

def UtilizadorEditarConfirmado():
    pass

def UtilizadorApagar():
    pass

def UtilizadorApagarConfirmado():
    pass


#Rotas para admin e utilizador
def ListarConsultas():
    #se é utilizador só lista as consultas do próprio
    pass


#erros


app.run(debug=True)