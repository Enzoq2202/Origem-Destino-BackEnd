from flask import Flask, request
import sqlite3
from pathlib import Path
import os
from dotenv import load_dotenv
from helpers.helpers import route_request, response_parser
import simplekml
from fastkml import kml
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)

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

# ------------------------------------------------- #

@app.route('/areas', methods=['GET'])
def kml_areas():

    kml_file = 'main/db/LL_WGS84_KMZ_distrito.kml'

    with open(kml_file, 'rb') as f:
        kml_document = f.read()

    k = kml.KML()
    k.from_string(kml_document)

    placemarks = []
    root = list(k.features())[0]  # Access the root feature (Document)
    folder = list(root.features())[0]  # Access the first nested feature (Folder)
    for feature in folder.features():  # Iterate over features within the nested Folder
        if isinstance(feature, kml.Placemark):
            placemarks.append(feature)

    areas = []
    for placemark in placemarks:
        newArea = {}
        newArea['name'] = str(placemark.name)
        newArea['coords'] = list(placemark.geometry.exterior.coords)
        areas.append(newArea)

    return { 'areas': areas }

if __name__ == '__main__':
    app.run(debug=True)