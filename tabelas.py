import basedados
import bcrypt

#Criar a base de dados e as tabelas
ligacao_bd=basedados.criar_conexao("vetonline.bd")

ativa_referencia_integridade="PRAGMA foreign_keys=ON"
basedados.executar_sql(ligacao_bd,ativa_referencia_integridade)

#Utilizadores(id,nome,morada,cp,data_nasc,email,password_hash,sal,perfil,token_recuperar,data_recuperar)
tabela_utilizadores="""
CREATE TABLE IF NOT EXISTS Utilizadores(
    id INTEGER PRIMARY KEY,
    nome text not null check (length(nome)>3),
    morada text,
    cp text,
    NIF text,
    data_nasc NUMERIC,
    email text not null unique check (email like '%@%.%'),
    password_hash text not null,
    sal text not null,
    perfil text not null,
    token_recuperar text,
    data_recuperar NUMERIC
)"""
basedados.executar_sql(ligacao_bd,tabela_utilizadores)

##############################################################
# Garantir que existe um utilizador admin
#############################################################
sql="SELECT count(*) as Contar FROM Utilizadores WHERE perfil='admin'"
dados=basedados.consultar_sql(ligacao_bd,sql)

if not dados or len(dados)<1 or dados[0]["contar"]==0:
    email="admin@gmail.com"
    nome="admin"
    palavra_passe="12345"
    palavra_passe=palavra_passe.encode('utf-8')
    #gerar sal
    sal = bcrypt.gensalt()
    #hash da palavra
    palavra_hash = bcrypt.hashpw(palavra_passe,sal)
    sql = """INSERT INTO Utilizadores(nome,email,password_hash,sal,perfil) VALUES
                (?,?,?,?,'admin')"""
    parametros=(nome,email,palavra_hash,sal)
    basedados.executar_sql(ligacao_bd,sql,parametros)

#Animais(id,nome,especie,raca,idade,data_nasc,peso,genero,id_utilizador)
tabela_animais="""
    CREATE TABLE IF NOT EXISTS Animais(
        id INTEGER PRIMARY KEY,
        nome TEXT,
        especie TEXT NOT NULL,
        raca TEXT,
        idade INTEGER,
        data_nasc NUMERIC,
        peso NUMERIC,
        genero TEXT CHECK (genero in ("f","F","m","M")),
        id_utilizador INTEGER REFERENCES Utilizadores(id)
    )
"""
basedados.executar_sql(ligacao_bd,tabela_animais)

#Consultas(id,id_animal,id_utilizador,data_marcacao,data_realizacao,estado,resumo)
tabela_consultas="""
    CREATE TABLE IF NOT EXISTS Consultas(
        id INTEGER PRIMARY KEY,
        id_animal INTEGER REFERENCES Animais(id),
        id_utilizador INTEGER REFERENCES Utilizadores(id),
        data_marcacao NUMERIC,
        data_realizacao NUMERIC,
        estado TEXT CHECK (estado in ("Pedida","Confirmada","Cancelada","Realizada")),
        resumo TEXT
    )
"""
basedados.executar_sql(ligacao_bd,tabela_consultas)