# nuevo_app.py

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2
from urllib.parse import urlparse

app = Flask(__name__)

# Obtener DATABASE_URL desde variables de entorno
DATABASE_URL = os.environ.get('DATABASE_URL')

# Si Heroku retorna URL con 'postgres', cambiarlo a 'postgresql'
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configurar la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or 'sqlite:///local.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo
class Intervencion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tecnico = db.Column(db.String(100))
    hospital = db.Column(db.String(200))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    maquina = db.Column(db.String(100))
    trabajo = db.Column(db.String(100))
    estado = db.Column(db.String(20), default='activo')

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/nueva', methods=['POST'])
def nueva_intervencion():
    data = request.json
    nueva = Intervencion(
        tecnico=data['tecnico'],
        hospital=data['hospital'],
        lat=data['lat'],
        lon=data['lon'],
        maquina=data['maquina'],
        trabajo=data['trabajo']
    )
    db.session.add(nueva)
    db.session.commit()
    return jsonify({'status': 'OK'})

@app.route('/finalizar/<int:id>', methods=['POST'])
def finalizar_intervencion(id):
    intervencion = Intervencion.query.get(id)
    if intervencion:
        intervencion.estado = 'finalizado'
        db.session.commit()
    return jsonify({'status': 'OK'})

@app.route('/intervenciones', methods=['GET'])
def obtener_intervenciones():
    activas = Intervencion.query.filter_by(estado='activo').all()
    return jsonify([
        {
            'id': i.id,
            'tecnico': i.tecnico,
            'hospital': i.hospital,
            'lat': i.lat,
            'lon': i.lon,
            'maquina': i.maquina,
            'trabajo': i.trabajo
        } for i in activas
    ])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



