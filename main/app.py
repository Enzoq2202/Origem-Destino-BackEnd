from flask import Flask, request
import sqlite3
from pathlib import Path


app = Flask(__name__)

# #Obtendo Path do DB
# FILE = Path(__file__).resolve()
# src_folder = FILE.parents[0]
# rel_arquivo_db = Path('db/cadastro.db')
# db = Path(src_folder / rel_arquivo_db).resolve()

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)