CREATE TABLE IF NOT EXISTS personas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar algunos datos de ejemplo
INSERT INTO personas (nombre, apellido, email, password_hash) VALUES
('Juan', 'Perez', 'juan.perez@example.com', 'hashed_password_1'),
('Maria', 'Gomez', 'maria.gomez@example.com', 'hashed_password_2');