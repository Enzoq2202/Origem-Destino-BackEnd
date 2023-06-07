# PTV-SP

Autores: Enzo Quental, Esdras Gomes, Júlia Karine, Júlia Paiva, Tomás Alessi

# Descrição 

O PTV-SP é uma ferramenta de análise origem-destino, para visualizar o deslocamento de professores na cidade de São Paulo. Com ela, é possível analisar:
 
- analisar rotas de deslocamento dos professores;
- visualizar meios de transporte utilizados;
- encontrar o tempo médio que o docente leva para chegar até a escola;
- detectar deslocamentos de grupos;
- inserir novas rotas;
- deletar rotas.

1. Como executar o projeto?

Acesse o link da versão executável do projeto: http://projeto-origem-destino.s3-website-sa-east-1.amazonaws.com/. Após clicar em "explorar", é possível visualizar o mapa com as rotas presentes na base de dados. Pode-se regular o zoom, filtrar por meio de transporte, entre outras funcionalidades.

2. Dependências

Construímos o backend em Flask e o frontend usando React e CSS. Como banco de dados, decidimos usar o Sqlite3. Em relação ao mapa, utilizamos o Leaflet, uma biblioteca em JavaScript de mapas interativos. A lista completa de dependências pode ser encontrada no arquivo "requirements.txt".

# Documentação

### Rotas

- /rota (GET)
    - Retorna uma lista de todas as rotas cadastradas na database. Consegue receber os argumentos: duration_min, duration_max, distance_min, distance_max, travel_mode.
- /rota (POST)
    - Recebe 5 argumentos, transforma esses dados em uma rota e salva ele na database. Argumentos: LatitudeOrigem, LongitudeOrigem, LatitudeDestino, LongitudeDestino, TravelMode.
- /rota (DELETE)
    - Remove todas as rotas da database.
- /rota/id (DELETE)
    - Remove a rota correspondente ao ID no url da database.
- /areas (GET)
    - Retorna uma lista de áreas de São Paulo (polígonos ditados por pontos no seu perímetro), com os seus respectivos nomes e regiôes.
- /macro (GET)
    - Retorna uma lista de rotas, onde o seu inicio é o ponto central de uma área e o final é centro de outra. Representa a migração de pessoas entre áreas diferentes, e tem um contador para quantidade de pessoas que se movimentam.
