#Gestão de consultas
import basedados
from flask import Flask, render_template, request, redirect, session
import datetime
import utilizadores

#Função que lista as consultas
def Listar():
    ligacao_bd=basedados.criar_conexao("vetonline.bd")
    if utilizadores.Utilizador_E_Admin():
        dados=basedados.consultar_sql(ligacao_bd,"SELECT * FROM Consultas")
    else:
        id_utilizador=session["id"]
        parametros=(id_utilizador,)
        dados=basedados.consultar_sql(ligacao_bd,"SELECT * FROM Consultas WHERE id_utilizador=?",parametros)
    return render_template("consultas/listar.html",registos=dados)

#Função para marcar uma consulta na base de dados
def marcar(estado):
    ligacao_bd=basedados.criar_conexao("vetonline.bd")
    if request.method=="GET":
        dados=basedados.consultar_sql(ligacao_bd,"SELECT id,nome FROM utilizadores order by nome")
        return render_template("consultas/marcar.html",utilizadores=dados)
    if request.method=="POST":
        id_utilizador=request.form.get("id_utilizador")
        id_animal=request.form.get("id_animal")
        data_consulta=request.form.get("data_realizacao")
        data_marcacao=datetime.datetime.now()
        razao=request.form.get("resumo")
        sql="INSERT INTO Consultas(id_utilizador,id_animal,data_realizacao,data_marcacao,resumo,estado) VALUES(?,?,?,?,?,?)"
        parametros=(id_utilizador,id_animal,data_consulta,data_marcacao,razao,estado)
        basedados.executar_sql(ligacao_bd,sql,parametros)
        return redirect("/Consultas/listar")
    

def alterarestado(id,estado):
    ligacao_bd=basedados.criar_conexao("vetonline.bd")
    sql="UPDATE Consultas SET estado=? WHERE id=?"
    dados=(estado,id)
    basedados.executar_sql(ligacao_bd,sql,dados)
    return redirect("/Consultas/listar")

def listarConsultasDia():
    ligacao_bd=basedados.criar_conexao("vetonline.bd")
    data_hoje=datetime.datetime.now()
    data_hoje=data_hoje.strftime("%Y-%m-%d")
    sql="SELECT * FROM Consultas WHERE data_realizacao=?"
    parametros=(data_hoje,)
    dados=basedados.consultar_sql(ligacao_bd,sql,parametros)
    return dados

def listarMinhasConsultas():
    ligacao_bd=basedados.criar_conexao("vetonline.bd")
    id_utilizador=session["id"]
    sql="SELECT * FROM Consultas WHERE id_utilizador=?"
    parametros=(id_utilizador,)
    dados=basedados.consultar_sql(ligacao_bd,sql,parametros)
    return dados