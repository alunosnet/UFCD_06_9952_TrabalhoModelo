import basedados

#Criar a base de dados e as tabelas
ligacao_bd=basedados.criar_conexao("vetonline.bd")

ativa_referencia_integridade="PRAGMA foreign_keys=ON"
basedados.executar_sql(ligacao_bd,ativa_referencia_integridade)

#Utilizadores(id,nome,morada,cp,data_nasc,email,password_hash,sal,perfil,token_recuperar,data_recuperar)
tabela_utilizadores="""
CREATE TABLE Utilizadores(
    id INTEGER PRIMARY KEY,
    nome text not null check (length(nome)>3),
    morada text,
    cp text,
    NIF text,
    data_nasc NUMERIC,
    email text not null check (email like '%@%.%'),
    password_hash text not null,
    sal text not null,
    perfil text not null,
    token_recuperar text,
    data_recuperar NUMERIC
)
"""
#Animais(id,nome,especie,raca,idade,data_nasc,peso,genero,id_utilizador)
tabela_animais=""""""

#Consultas(id,id_animal,id_utilizador,data_marcacao,data_realizacao,estado,resumo)
tabela_consultas=""