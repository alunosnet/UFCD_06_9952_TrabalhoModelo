import basedados

#Criar a base de dados e as tabelas
ligacao_bd=basedados.criar_conexao("vetonline.bd")

ativa_referencia_integridade="PRAGMA foreign_keys=ON"
basedados.executar_sql(ligacao_bd,ativa_referencia_integridade)

