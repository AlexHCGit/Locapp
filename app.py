# archivo: app.py

from flask import Flask, request, jsonify
import sqlite3

from flask import render_template


app = Flask(__name__)
DB = "localizacion.db"

# Inicializar base de datos
def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS intervenciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tecnico TEXT,
                hospital TEXT,
                lat REAL,
                lon REAL,
                maquina TEXT,
                trabajo TEXT,
                estado TEXT
            )
        ''')
    print("Base de datos inicializada.")

@app.route('/nueva', methods=['POST'])
def nueva_intervencion():
    data = request.json
    with sqlite3.connect(DB) as conn:
        conn.execute('''
            INSERT INTO intervenciones (tecnico, hospital, lat, lon, maquina, trabajo, estado)
            VALUES (?, ?, ?, ?, ?, ?, 'activo')
        ''', (data['tecnico'], data['hospital'], data['lat'], data['lon'], data['maquina'], data['trabajo']))
    return jsonify({'status': 'OK'})

@app.route('/finalizar/<int:id>', methods=['POST'])
def finalizar_intervencion(id):
    with sqlite3.connect(DB) as conn:
        conn.execute('UPDATE intervenciones SET estado = "finalizado" WHERE id = ?', (id,))
    return jsonify({'status': 'OK'})

@app.route('/intervenciones', methods=['GET'])
def intervenciones():
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM intervenciones WHERE estado = "activo"')
        rows = cur.fetchall()
    intervenciones = [
        {'id': row[0], 'tecnico': row[1], 'hospital': row[2], 'lat': row[3], 'lon': row[4], 'maquina': row[5], 'trabajo': row[6]}
        for row in rows
    ]
    return jsonify(intervenciones)

@app.route('/')
def home():
    return render_template('index.html')



if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)


