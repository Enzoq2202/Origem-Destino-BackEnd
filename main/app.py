from flask import Flask, request
import sqlite3
from pathlib import Path
import os
from dotenv import load_dotenv
from helpers.helpers import route_request, response_parser
from flask import request

app = Flask(__name__)

#Obtendo Path do DB
FILE = Path(__file__).resolve()
src_folder = FILE.parents[0]
rel_arquivo_db = Path('db/maps.db')
db = Path(src_folder / rel_arquivo_db).resolve()

# Obtendo API_KEY do .env
load_dotenv()
api_key = os.getenv("API_KEY")



@app.route('/rota', methods=['POST'])
def rota():
    #Obtendo dados do POST
    data = request.get_json()

    #Criando a conexão com o banco de dados
    conn = sqlite3.connect(db)

    # Fazendo a requisição na API do Google Maps
    response = route_request(data['LatitudeOrigem'], data['LongitudeOrigem'],data['LatitudeDestino'],data['LongitudeDestino'],data['TravelMode'], api_key)
    print(response)

    #Parseando a resposta
    parsed_response = response_parser(response)


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
        parsed_response['EncodedRoutes'][0],
        parsed_response['DistanceMeters'][0],
        parsed_response['Duration'][0]
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
    
    #Obtendo os valor dos parâmetro da query
    travel_mode = request.args.get('travel_mode')
 
    duration_max = request.args.get('duration_max')

    duration_min= request.args.get('duration_min')
    #Criando lista de rotas
    rotas = []

    #Percorrendo dados da tabela
    for row in cursor:
        # filtrnado por modo de viagem
        if travel_mode is None or travel_mode == row[5]:
            # filtrando por duração minimia
            if duration_min == None or duration_min <= row[8]:
                # filtrando por duração máxima
                if duration_max == None or duration_max >= row[8]:
        
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
                        'duration': row[8],

                    }

                    #Adicionando rota na lista de rotas
                    rotas.append(rota)

    #Fecha a conexão
    conn.close()
    #Retorna lista de rotas
    return {'rotas': rotas}



if __name__ == '__main__':
    app.run(debug=True)