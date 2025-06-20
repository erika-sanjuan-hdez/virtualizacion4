# Ejemplo básico de Flask API (requiere 'Flask' en requirements.txt)
from flask import Flask, jsonify, request
import psycopg2
import os

app = Flask(__name__)

DB_NAME = os.getenv('DB_NAME', 'personas_db')
DB_USER = os.getenv('DB_USER', 'admin')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_strong_password')
DB_HOST = os.getenv('DB_HOST', 'db-server.unam.local') # Usar el hostname resuelto por DNS
DB_PORT = os.getenv('DB_PORT', '5432')

def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

@app.route('/personas', methods=['GET'])
def get_personas():
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, apellido, email FROM personas")
        personas = cur.fetchall()
        return jsonify([
            {"id": p[0], "nombre": p[1], "apellido": p[2], "email": p[3]}
            for p in personas
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cur: cur.close()
        if conn: conn.close()

@app.route('/personas', methods=['POST'])
def add_persona():
    data = request.json
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    email = data.get('email')
    password_hash = data.get('password_hash') # En una app real, esto se hashea

    if not all([nombre, apellido, email, password_hash]):
        return jsonify({"error": "Faltan datos"}), 400

    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO personas (nombre, apellido, email, password_hash) VALUES (%s, %s, %s, %s)",
            (nombre, apellido, email, password_hash)
        )
        conn.commit()
        return jsonify({"message": "Persona agregada exitosamente"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cur: cur.close()
        if conn: conn.close()

if __name__ == '__main__':
    # Para desarrollo, usar gunicorn para producción
    app.run(host='0.0.0.0', port=5000)