import sqlite3


# Criando a conexão com o banco de dados
conn = sqlite3.connect('main/db/maps.db')

conn.execute('''CREATE TABLE MinhaTabela (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    LatitudeOrigem REAL,
    LongitudeOrigem REAL,
    LatitudeDestino REAL,
    LongitudeDestino REAL,
    TravelMode TEXT,
    EncodedRoutes TEXT,
    DistanceMeters REAL,
    Duration TEXT,
    Area TEXT
);''')





# Salva as alterações
conn.commit()

# Fecha a conexão
conn.close()