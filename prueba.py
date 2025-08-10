class Index:
    def GET(self):
        return render.registro()
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
        last_id = self.cursor.lastrowid
        self.conn.close()
        return last_id

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
        last_id = self.cursor.lastrowid
        self.conn.close()
        return last_id

# Configuración de rutas web.py
urls = (
    '/', 'Index',
    '/registro', 'Registro',
    '/login', 'Login',
    '/registro_completo', 'RegistroCompletoWeb',
    '/recuperar_contrasena', 'RecuperarContrasena',

)

class RecuperarContrasena:
    def GET(self):
        return render.recuperar_contrasena()
    def POST(self):
        data = web.input()
        correo = data.correo
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT contraseña_texto FROM registro_usuario WHERE correo=?", (correo,))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            contrasena = resultado[0]
            return f"Tu contraseña es: <b>{contrasena}</b> <br><a href='/login'>Volver al login</a>"
        else:
            return "Correo no encontrado. <a href='/recuperar_contrasena'>Intentar de nuevo</a>"
class Login:
    def GET(self):
        return render.login()
    def POST(self):
        data = web.input()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM registro_usuario WHERE correo=? AND contraseña_texto=?", (data.correo, data.contrasena))
        usuario = cursor.fetchone()
app = web.application(urls, globals())

# Clase para registro conjunto
class RegistroCompletoWeb:
    def GET(self):
        return render.registro()
    def POST(self):
        data = web.input()
        usuario = RegistroUsuario()
        id_usuario = usuario.crear_usuario(
            data.nombre, data.apellidos, data.correo, data.contrasena, data.tipo_usuario
        )
        ninos = RegistroNino()
        nombres_ninos = data.get('nombre_nino[]', [])
        apellidos_ninos = data.get('apellidos_nino[]', [])
        edades_ninos = data.get('edad_nino[]', [])
        generos_ninos = data.get('genero_nino[]', [])
        if not isinstance(nombres_ninos, list):
            nombres_ninos = [nombres_ninos]
            apellidos_ninos = [apellidos_ninos]
            edades_ninos = [edades_ninos]
            generos_ninos = [generos_ninos]
        for nombre, apellidos, edad, genero in zip(nombres_ninos, apellidos_ninos, edades_ninos, generos_ninos):
            ninos.crear_nino(nombre, apellidos, int(edad), genero, True, id_usuario)
        return render.registro_exito()
render = web.template.render('templates/')

if __name__ == "__main__":
    app.run()

