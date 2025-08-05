import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'registro.db')

# Crear tablas si no existen
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS registro_usuario (
    id_registro_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    primer_apellido_y_segundo_apellido TEXT,
    correo TEXT UNIQUE,
    contraseña_texto TEXT,
    fecha_registro DATE,
    tipo_usuario TEXT CHECK (tipo_usuario IN ('padre/madre', 'tutor', 'profesor'))
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS niños (
    id_niño INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    primer_apellido_y_segundo_apellido TEXT,
    edad INTEGER CHECK (edad >= 0),
    género TEXT,
    agregar_niños BOOLEAN,
    id_registro_usuario1 INTEGER,
    FOREIGN KEY (id_registro_usuario1) REFERENCES registro_usuario(id_registro_usuario)
        ON DELETE CASCADE
)
''')

conn.commit()
conn.close()
print("Tablas creadas o ya existen.")
