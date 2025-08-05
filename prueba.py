import web
import sqlite3
import os
from datetime import datetime

# Configuración de la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), 'registro.db')

# Clase para manejar el registro de usuarios (padre/tutor)
class RegistroUsuario:
    def __init__(self, db_path=DB_PATH):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def crear_usuario(self, nombre, apellidos, correo, contrasena, tipo_usuario):
        fecha_registro = datetime.now().strftime('%Y-%m-%d')
        self.cursor.execute('''
            INSERT INTO registro_usuario (nombre, primer_apellido_y_segundo_apellido, correo, contraseña_texto, fecha_registro, tipo_usuario)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, apellidos, correo, contrasena, fecha_registro, tipo_usuario))
        self.conn.commit()
        return self.cursor.lastrowid

# Clase para manejar el registro de niños
NINOS_DB_PATH = os.path.join(os.path.dirname(__file__), 'niños.db')
class RegistroNino:
    def __init__(self, db_path=NINOS_DB_PATH):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def crear_nino(self, nombre, apellidos, edad, genero, agregar_niños, id_registro_usuario1):
        self.cursor.execute('''
            INSERT INTO niños (nombre, primer_apellido_y_segundo_apellido, edad, género, agregar_niños, id_registro_usuario1)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, apellidos, edad, genero, agregar_niños, id_registro_usuario1))
        self.conn.commit()
        return self.cursor.lastrowid

# Configuración de rutas web.py
urls = (
    '/', 'Index',
    '/registro', 'Registro',
)

app = web.application(urls, globals())

render = web.template.render('templates/')

class Index:
    def GET(self):
        return render.registro()

class Registro:
    def POST(self):
        data = web.input()
        # DEBUG: Mostrar lo que recibe el backend
        print('DATA RECIBIDA:', dict(data))
        # Registro de usuario
        usuario = RegistroUsuario()
        id_usuario = usuario.crear_usuario(
            data.nombre, data.apellidos, data.correo, data.contrasena, data.tipo_usuario
        )
        # Registro de niños (puede ser uno o varios)
        ninos = RegistroNino()
        # Suponiendo que los datos de niños vienen como listas
        nombres_ninos = data.get('nombre_nino[]', [])
        apellidos_ninos = data.get('apellidos_nino[]', [])
        edades_ninos = data.get('edad_nino[]', [])
        generos_ninos = data.get('genero_nino[]', [])
        # Normalizar a listas
        if not isinstance(nombres_ninos, list):
            nombres_ninos = [nombres_ninos]
            apellidos_ninos = [apellidos_ninos]
            edades_ninos = [edades_ninos]
            generos_ninos = [generos_ninos]
        print('NINOS:', nombres_ninos, apellidos_ninos, edades_ninos, generos_ninos)
        # Registrar cada niño
        for nombre, apellidos, edad, genero in zip(nombres_ninos, apellidos_ninos, edades_ninos, generos_ninos):
            print('Registrando niño:', nombre, apellidos, edad, genero)
            ninos.crear_nino(nombre, apellidos, int(edad), genero, True, id_usuario)
        return "Registro exitoso."

if __name__ == "__main__":
    app.run()

