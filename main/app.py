from flask import Flask, make_response, request
import sqlite3
from pathlib import Path
import os, random
from dotenv import load_dotenv
from helpers.helpers import route_request, response_parser
from fastkml import kml
from flask_cors import CORS  
from shapely.geometry import Point, Polygon

print('Iniciando API...')
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


# ------------------------------------------------- #

@app.route('/rota', methods=['POST'])
def rota():
    # Obtendo dados do POST
    data = request.get_json()

    # Criando a conexão com o banco de dados
    conn = sqlite3.connect(db)

    # Fazendo a requisição na API do Google Maps
    response = route_request(
        data['LatitudeOrigem'],
        data['LongitudeOrigem'],
        data['LatitudeDestino'],
        data['LongitudeDestino'],
        data['TravelMode'],
        api_key
    )

    # Parseando a resposta
    parsed_response = response_parser(response)

    # Verificando se a lista de EncodedRoutes está vazia
    encoded_routes = parsed_response['EncodedRoutes']
    if encoded_routes:
        encoded_route = encoded_routes[0]
    else:
        encoded_route = ''

    # Verificando região origem
    p1 = Point(data['LongitudeOrigem'], data['LatitudeOrigem'])
    areaOrig = 'none'
    respArea = kml_areas()['areas']
    for area in respArea:
        poly = Polygon(area['coords'])
        if poly.contains(p1):
            areaOrig = area['name']

    # Verificando região destino
    p2 = Point(data['LongitudeDestino'], data['LatitudeDestino'])
    areaDest = 'none'
    respArea = kml_areas()['areas']
    for area in respArea:
        poly = Polygon(area['coords'])
        if poly.contains(p2):
            areaDest = area['name']

    # Inserindo dados na tabela
    conn.execute(
        '''INSERT INTO MinhaTabela (
        LatitudeOrigem,
        LongitudeOrigem,
        LatitudeDestino,
        LongitudeDestino,
        TravelMode,
        EncodedRoutes,
        DistanceMeters,
        Duration,
        AreaOrigem,
        AreaDestino
    ) VALUES (?,?,?,?,?,?,?,?,?,?)''', (
            data['LatitudeOrigem'],
            data['LongitudeOrigem'],
            data['LatitudeDestino'],
            data['LongitudeDestino'],
            data['TravelMode'],
            encoded_route,
            parsed_response['DistanceMeters'][0] if parsed_response['DistanceMeters'] else '',
            parsed_response['Duration'][0] if parsed_response['Duration'] else '',
            areaOrig,
            areaDest
        )
    )

    # Salva as alterações
    conn.commit()

    # Fecha a conexão
    conn.close()
    response = make_response("Rota adicionada com sucesso!")
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# ------------------------------------------------- #

@app.route('/rota', methods=['GET'])
def rotas():
    # Obtendo o travelMode dos parâmetros da query
    travel_mode = request.args.get('travelMode')
    
    # Criando a conexão com o banco de dados
    conn = sqlite3.connect(db)
    # Obtendo dados da tabela
    cursor = conn.execute('''SELECT * FROM MinhaTabela WHERE TravelMode = ?''', (travel_mode,)) if travel_mode else conn.execute('''SELECT * FROM MinhaTabela''')
    
    #Obtendo os valor dos parâmetro da query
    travel_mode = request.args.get('travel_mode')
 
    duration_max = request.args.get('duration_max')
    duration_min= request.args.get('duration_min')
    # Criando lista de rotas
    rotas = []
    # Percorrendo dados da tabela
    for row in cursor:
        # filtrnado por modo de viagem
        if travel_mode is None or travel_mode == row[5]:
            # filtrando por duração minimia
            if duration_min == None or duration_min <= row[8]:
                # filtrando por duração máxima
                if duration_max == None or duration_max >= row[8]:
        
                    # Criando dicionário de rota
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
                        'areaOrigem': row[9],
                        'areaDestino': row[10]
                    }

                    # Adicionando rota na lista de rotas


                    rotas.append(rota)
    # Fecha a conexão
    conn.close()

    # Retorna lista de rotas
    response = make_response({'rotas': rotas})
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# ------------------------------------------------- #

@app.route('/areas', methods=['GET'])
def kml_areas():

    kml_file = 'main\db\LL_WGS84_KMZ_distrito.kml'

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
        newArea['name'] = str(placemark.extended_data.elements[0].data[0]['value']) + ' - ' + str(placemark.extended_data.elements[0].data[3]['value']) 
        newArea['coords'] = list(placemark.geometry.exterior.coords)
        areas.append(newArea)

    return { 'areas': areas }

# ------------------------------------------------- #

app.route('/rota/<int:id>/', methods=['DELETE'])
def delete_rota(id):
    #Criando a conexão com o banco de dados
    conn = sqlite3.connect(db)

    #Deletando rota
    conn.execute('''DELETE FROM MinhaTabela WHERE id = ?''', (id,))

    #Salva as alterações
    conn.commit()

    #Fecha a conexão
    conn.close()

    return "Rota deletada com sucesso!"

app.add_url_rule('/rota/<int:id>/', view_func=delete_rota, methods=['DELETE'])

# ------------------------------------------------- #

@app.route('/rota', methods=['DELETE'])
def delete_todas_rotas():
    #Criando a conexão com o banco de dados
    conn = sqlite3.connect(db)

    #Deletando rota
    conn.execute('''DELETE FROM MinhaTabela''')

    #Salva as alterações
    conn.commit()

    #Fecha a conexão
    conn.close()

    return "Todas as rotas foram deletadas com sucesso!"

# ------------------------------------------------- #

@app.route('/macro', methods=['GET'])
def macroAreas():

    areasDict = kml_areas()["areas"]
    midpoints = {}
    for area in areasDict:
        poly = Polygon(area['coords'])
        point = poly.centroid
        midpoints[area['name']] = [point.x, point.y]

    conn = sqlite3.connect(db)
    cursor = conn.execute('''SELECT * FROM MinhaTabela''')

    areaRoutes = []
    addedPaths = []
    for row in cursor:

        start = row[9]
        end = row[10]
        name = start +" // "+ end

        if (start != end) and (start != 'none') and (end != 'none'):

            if name not in addedPaths:
                addedPaths.append(name)

                startCoords = midpoints[start]
                endCoords = midpoints[end]
                
                offset = (random.randint(0, 2)-1)/1000
                midpoint = [(startCoords[0]+endCoords[0])/2 +offset, (startCoords[1]+endCoords[1])/2 +offset]
                path = [startCoords, midpoint, endCoords]

                newDict = {'route': path, 'name': name, 'people':1}
                areaRoutes.append(newDict)

            else:
                for item in areaRoutes:
                    if item['name'] == name:
                        item['people'] += 1

    conn.close()
    return {'routes': areaRoutes}

# ------------------------------------------------- #

if __name__ == '__main__':
    app.run(debug=True)