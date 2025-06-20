import psycopg2
import os

DB_NAME = os.getenv('DB_NAME', 'personas_db')
DB_USER = os.getenv('DB_USER', 'admin')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_strong_password') # Usar una variable de entorno o vault
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

def insert_person(nombre, apellido, email, password_hash):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO personas (nombre, apellido, email, password_hash) VALUES (%s, %s, %s, %s)",
            (nombre, apellido, email, password_hash)
        )
        conn.commit()
        print(f"Persona {nombre} {apellido} insertada.")
    except Exception as e:
        conn.rollback()
        print(f"Error al insertar persona: {e}")
    finally:
        cur.close()
        conn.close()

def fetch_all_people():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, nombre, apellido, email FROM personas")
        people = cur.fetchall()
        for person in people:
            print(person)
        return people
    except Exception as e:
        print(f"Error al consultar personas: {e}")
        return []
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    # Ejemplo de uso
    insert_person('Alice', 'Smith', 'alice.smith@example.com', 'hashed_alice')
    insert_person('Bob', 'Johnson', 'bob.johnson@example.com', 'hashed_bob')
    print("\nPersonas en la base de datos:")
    fetch_all_people()