
from flask import Flask, render_template, request, redirect, session,make_response, jsonify
from flask_mail import Mail, Message
import utilizadores
import basedados

def setup_public_routes(app,mail):
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

    @app.route('/recuperar_password',methods=['POST','GET'])
    def RecuperarPassword():
        token=request.args.get("token",None)
        #se o utilizador não tem token (1º passo)
        if token is None and request.method=="GET":
            #enviar email para utilizador com o token
            email_destino=request.args.get("email")
            token = str(utilizadores.CriarToken(email_destino))
            assunto="Recuperação de palavra passe"
            texto="Clique no link para redefinir a sua palavra passe <a href='http://127.0.0.1:5000/recuperar_password?token="+token+"'>Clique aqui</a>"
            mensagem=Message(assunto,sender="meu_email@gmail.com",recipients=[email_destino])
            mensagem.body=texto
            mensagem.html=texto
            mail.send(mensagem)
            return render_template("index.html",mensagem="Email de recuperação da palavra passe enviado.")
        else:
            #se o utilizador tem token (2º passo)
            #o pedido é um get
            if request.method=="GET":
                return render_template("utilizadores/recuperar_password.html",token=token,site_key=utilizadores.RECAPTCHA_SITE_KEY)
            else:
                #o utilizador tem token e o pedido é um post (3º passo)
                token=request.form.get("token")
                password=request.form.get("password")
                return utilizadores.Nova_Password(token,password)
                #return render_template("index.html",mensagem="Palavra passe alterada com sucesso.")
