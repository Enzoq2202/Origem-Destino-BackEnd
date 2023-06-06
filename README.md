# PTV-SP

Autores: Enzo Quental, Esdras Gomes, Júlia Karine, Júlia Paiva, Tomás Alessi

# Descrição 

O PTV-SP é uma ferramenta de análise origem-destino, para visualizar o deslocamento de professores na cidade de São Paulo. Com ela, é possível analisar:
 
- rotas de deslocamento dos professores;
- meios de transporte utilizados;
- tempo médio que o docente leva para chegar até a escola;
- deslocamentos de grupos.

1. Como executar o projeto?

Acesse o link da versão executável do projeto: http://projeto-origem-destino.s3-website-sa-east-1.amazonaws.com/. Após clicar em "explorar", é possível visualizar o mapa com as rotas presentes na base de dados. Pode-se regular o zoom, filtrar por meio de transporte, entre outras funcionalidades.

2. Dependências

Construímos o backend em Flask e o frontend usando React e CSS. Como banco de dados, decidimos usar o Sqlite3. Em relação ao mapa, utilizamos o Leaflet, uma biblioteca em JavaScript de mapas interativos. A lista completa de dependências pode ser encontrada no arquivo "requirements.txt".