CREATE TABLE orientacion_habitacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    orientacion VARCHAR(50)
);

CREATE TABLE habitacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_habitacion INT NOT NULL,
    pasajeros_admitidos INT NOT NULL,
    id_orientacion INT,
    id_pasajero INT,
    estado ENUM('ocupada', 'vacante') DEFAULT 'vacante',
    FOREIGN KEY (id_orientacion) REFERENCES orientacion_habitacion(id),
);

CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL,
    contraseña VARCHAR(244) NOT NULL,
    cargo ENUM('Encargado', 'Administrador') NOT NULL
);

CREATE TABLE pasajero (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL,
    apellido VARCHAR(60) NOT NULL,
    rut VARCHAR(20) NOT NULL UNIQUE,
    id_habitacion INT,
    FOREIGN KEY (id_habitacion) REFERENCES habitacion(id)
);

CREATE TABLE reserva (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_habitacion INT,
    id_pasajero_responsable INT,
    fechaHora_asignacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    costo_total DECIMAL(10, 2) NOT NULL,
    id_usuario INT,
    FOREIGN KEY (id_habitacion) REFERENCES habitacion(id),
    FOREIGN KEY (id_pasajero_responsable) REFERENCES pasajero(id),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
);

CREATE TABLE pasajero_habitacion (
    id_pasajero INT,
    id_habitacion INT,
    responsable TINYINT(1) NOT NULL,
    PRIMARY KEY (id_pasajero, id_habitacion),
    FOREIGN KEY (id_pasajero) REFERENCES pasajero(id),
    FOREIGN KEY (id_habitacion) REFERENCES habitacion(id)
);