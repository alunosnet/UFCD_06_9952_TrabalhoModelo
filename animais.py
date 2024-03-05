#Gestão dos animais
import basedados
from flask import Flask, render_template, request, redirect, session



#Função para adicionar um animal novo na base de dados
def Adicionar(app):
    ligacao_bd=basedados.criar_conexao("vetonline.bd")
    if request.method=="GET":
        dados=basedados.consultar_sql(ligacao_bd,"SELECT id,nome FROM utilizadores ORDER BY Nome")
        return render_template("animais/adicionar.html",utilizadores=dados)
    if request.method=="POST":
        nome=request.form.get("nome")
        especie=request.form.get("especie")
        raca=request.form.get("raca")
        idade=request.form.get("idade")
        data_nasc=request.form.get("data_nasc")
        peso=request.form.get("peso")
        genero=request.form.get("genero")
        id_utilizador=request.form.get("id_utilizador")
        sql="INSERT INTO Animais(nome,especie,raca,idade,data_nasc,peso,genero,id_utilizador) VALUES(?,?,?,?,?,?,?,?)"
        parametros=(nome,especie,raca,idade,data_nasc,peso,genero,id_utilizador)
        id_animal=basedados.executar_sql(ligacao_bd,sql,parametros)
        if id_animal is None:
            dados=basedados.consultar_sql(ligacao_bd,"SELECT id,nome FROM utilizadores ORDER BY Nome")
            return render_template("animais/adicionar.html",mensagem="Erro ao adicionar o animal",utilizadores=dados)
        #fotografia
        fotografia=request.files["fotografia"]
        nome_fotografia=f"{id_animal}.jpg"
        fotografia.save(app.config['UPLOAD_FOLDER']+"/"+nome_fotografia)
        return redirect("/Animais/listar")

def Listar(app):
    ligacao_bd=basedados.criar_conexao("vetonline.bd")
    dados=basedados.consultar_sql(ligacao_bd,"SELECT * FROM Animais")
    return render_template("animais/listar.html",registos=dados)