import sqlite3


# Criando a conexão com o banco de dados
conn = sqlite3.connect('maps.db')


# Salva as alterações
conn.commit()

# Fecha a conexão
conn.close()