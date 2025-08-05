-- Tabla principal de usuarios
CREATE TABLE registro_usuario (
    id_registro_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    primer_apellido_y_segundo_apellido TEXT,
    correo TEXT UNIQUE,
    contraseña_texto TEXT,
    fecha_registro DATE,
    tipo_usuario TEXT CHECK (tipo_usuario IN ('padre/madre', 'tutor', 'profesor'))
);

-- Tabla de niños
CREATE TABLE niños (
    id_niño INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    primer_apellido_y_segundo_apellido TEXT,
    edad INTEGER CHECK (edad >= 0),
    género TEXT,
    agregar_niños BOOLEAN,
    id_registro_usuario1 INTEGER,
    FOREIGN KEY (id_registro_usuario1) REFERENCES registro_usuario(id_registro_usuario)
        ON DELETE CASCADE
);

-- Tabla de rachas
CREATE TABLE racha (
    id_racha INTEGER PRIMARY KEY AUTOINCREMENT,
    id_niño INTEGER,
    días_consecutivos INTEGER CHECK (días_consecutivos >= 0),
    ultima_fecha_activa DATE,
    FOREIGN KEY (id_niño) REFERENCES niños(id_niño)
        ON DELETE CASCADE
);

-- Tabla de contraseña de figuras
CREATE TABLE contraseña_figuras (
    id_contraseña INTEGER PRIMARY KEY AUTOINCREMENT,
    id_niño INTEGER,
    figura TEXT CHECK (figura IN ('triángulo', 'cuadrado', 'círculo')),
    orden INTEGER CHECK (orden >= 1),
    valor_asignado TEXT,
    FOREIGN KEY (id_niño) REFERENCES niños(id_niño)
        ON DELETE CASCADE
);

-- Tabla de recuperación de token
CREATE TABLE token_recuperacion (
    id_token INTEGER PRIMARY KEY AUTOINCREMENT,
    id_registro_usuario INTEGER,
    token TEXT UNIQUE,
    fecha_expiracion DATETIME,
    usado BOOLEAN DEFAULT 0,
    FOREIGN KEY (id_registro_usuario) REFERENCES registro_usuario(id_registro_usuario)
        ON DELETE CASCADE
);
