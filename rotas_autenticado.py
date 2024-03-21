from flask import Flask, render_template, request, redirect, session,make_response, jsonify
from flask_session import Session
import utilizadores, consultas, animais
import basedados

def setup_auth_routes(app):
    #Rotas para user logado
    @app.route('/Logout')
    def Logout():
        return utilizadores.Logout()

################################################################  >>>  Consultas
    @app.route("/Consultas/marcar",methods=["POST","GET"])
    def MarcarConsulta():
        if utilizadores.Logado():
            if utilizadores.Utilizador_E_Admin():
                return consultas.marcar("Confirmada")
            else:
                return consultas.marcar("Pedida")
        return redirect("/")


    @app.route("/Consultas/listar",methods=['GET'])
    def ConsultasListar():
        if utilizadores.Logado():
            return consultas.Listar()
        return redirect("/")

    @app.route("/Consultas/confirmar",methods=["POST"])
    def ConsultasConfirmar():
        if utilizadores.Utilizador_E_Admin()==False:
            return redirect("/")
        id=request.form.get("id")
        estado="Confirmada"
        return consultas.alterarestado(id,estado)

    @app.route("/Consultas/cancelar",methods=["POST"])
    def ConsultasCancelar():
        if utilizadores.Utilizador_E_Admin()==False:
            return redirect("/")
        id=request.form.get("id")
        estado="Cancelada"
        return consultas.alterarestado(id,estado);
    
    @app.route("/Consultas/realizada",methods=["POST"])
    def ConsultasRealizada():
        if utilizadores.Utilizador_E_Admin()==False:
            return redirect("/")
        id=request.form.get("id")
        estado="Realizada"
        return consultas.alterarestado(id,estado);

################################################################ >>>> Animais
    #Rotas para user admin
    @app.route("/Animais/adicionar",methods=["POST","GET"])
    def AnimaisAdicionar():
        if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
            return redirect("/")
        return animais.Adicionar(app)

    @app.route("/Animais/listar")
    def AnimaisListar():
        if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
            return redirect("/")
        return animais.Listar(app)
    
    @app.route("/Animais/apagar",methods=["POST"])
    def AnimaisApagar():
        if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
            return redirect("/")
        return animais.Apagar()
    
    @app.route("/Animais/apagar_confirmado",methods=["POST"])
    def AnimaisApagarConfirmado():
        if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
            return redirect("/")
        return animais.ApagarConfirmado()

    @app.route("/Animais/editar",methods=["POST"])
    def AnimaisEditar():
        if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
            return redirect("/")
        return animais.Editar()

    @app.route("/Animais/editar_confirmado",methods=["POST"])
    def AnimaisEditarConfirmado():
        if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
            return redirect("/")
        return animais.EditarConfirmado(app)
    
    @app.route("/Animais/pesquisar",methods=["GET","POST"])
    def AnimaisPesquisar():
        if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
            return redirect("/")
        if request.method=="GET":
            return render_template("animais/pesquisar.html",registos=[])
        else:
            especie=request.form.get("especie")
            sql="SELECT * FROM Animais WHERE especie like ?"
            especie = "%"+especie+"%"
            ligacao_bd=basedados.criar_conexao("vetonline.bd")
            parametros=(especie,)
            dados=basedados.consultar_sql(ligacao_bd,sql,parametros)
            return render_template("animais/pesquisar.html",registos=dados)


################################################################ >>>> Utilizadores


    @app.route("/Utilizadores/adicionar",methods=["POST","GET"])
    def UtilizadorAdicionar():
        if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
            return redirect("/")
        return utilizadores.Adicionar()

    @app.route("/Utilizadores/listar")
    def UtilizadorListar():
        if utilizadores.Logado()==False:
            return redirect("/")
        return utilizadores.Listar()

    @app.route("/Utilizadores/perfil",methods=["POST","GET"])
    def UtilizadoresPerfil():
        if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
            return redirect("/")
        return utilizadores.MudarPerfil()

    @app.route("/Utilizadores/bloquear",methods=["POST","GET"])
    def UtilizadorBloquear():
        if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
            return redirect("/")
        return utilizadores.Bloquear()

    @app.route("/Utilizadores/editar",methods=["POST","GET"])
    def UtilizadorEditar():
        if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
            return redirect("/")
        return utilizadores.Editar()

    @app.route("/Utilizadores/editar_confirmado",methods=["POST","GET"])
    def UtilizadorEditarConfirmado():
        if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
            return redirect("/")
        return utilizadores.EditarConfirmado()

    @app.route("/Utilizadores/apagar",methods=["POST","GET"])
    def UtilizadorApagar():
        if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
            return redirect("/")
        return utilizadores.Apagar()

    @app.route("/Utilizadores/apagar_confirmado",methods=["POST","GET"])
    def UtilizadorApagarConfirmado():
        if utilizadores.Logado()==False or utilizadores.Utilizador_E_Admin()==False:
            return redirect("/")
        return utilizadores.ApagarConfirmado()

    @app.route("/Perfil",methods=["GET"])
    def EditarPerfil():
        if utilizadores.Logado()==False:
            return redirect("/")
        return utilizadores.EditarPerfil()

    @app.route("/Utilizadores/perfil_confirmado",methods=["POST"])
    def PerfilConfirmado():
        if utilizadores.Logado()==False:
            return redirect("/")
        return utilizadores.EditarConfirmado()


