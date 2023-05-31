from flask import Flask, request
import sqlite3
from pathlib import Path


app = Flask(__name__)

#Obtendo Path do DB
FILE = Path(__file__).resolve()
src_folder = FILE.parents[0]
rel_arquivo_db = Path('db/maps.db')
db = Path(src_folder / rel_arquivo_db).resolve()


@app.route('/rota', methods=['POST'])
def rota():
    #Obtendo dados do POST
    data = request.get_json()
    print(data)

    #Criando a conexão com o banco de dados
    conn = sqlite3.connect(db)

    #Inserindo dados na tabela
    conn.execute('''INSERT INTO MinhaTabela (
        LatitudeOrigem,
        LongitudeOrigem,
        LatitudeDestino,
        LongitudeDestino,
        TravelMode,
        EncodedRoutes,
        DistanceMeters,
        Duration
    ) VALUES (?,?,?,?,?,?,?,?)''', (
        data['LatitudeOrigem'],
        data['LongitudeOrigem'],
        data['LatitudeDestino'],
        data['LongitudeDestino'],
        data['TravelMode'],
        data['EncodedRoutes'],
        data['DistanceMeters'],
        data['Duration']
    ))

    #Salva as alterações
    conn.commit()

    #Fecha a conexão
    conn.close()

    return "Rota adicionada com sucesso!"

@app.route('/rota', methods=['GET'])
def rotas():
    #Criando a conexão com o banco de dados
    conn = sqlite3.connect(db)

    #Obtendo dados da tabela
    cursor = conn.execute('''SELECT * FROM MinhaTabela''')

    #Criando lista de rotas
    rotas = []

    #Percorrendo dados da tabela
    for row in cursor:
        #Criando dicionário de rota
        rota = {
            'id': row[0],
            'latitudeOrigem': row[1],
            'longitudeOrigem': row[2],
            'latitudeDestino': row[3],
            'longitudeDestino': row[4],
            'travelMode': row[5],
            'encodedRoutes': row[6],
            'distanceMeters': row[7],
            'duration': row[8]
        }

        #Adicionando rota na lista de rotas
        rotas.append(rota)

    #Fecha a conexão
    conn.close()

    #Retorna lista de rotas
    return {'rotas': rotas}



if __name__ == '__main__':
    app.run(debug=True)