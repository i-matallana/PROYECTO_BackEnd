-- Creacion de base datos
 create database sportpoint_db;
 
 use sportpoint_db;
 
CREATE TABLE usuario (
    id_usuario VARCHAR(36) NOT NULL,
    correo VARCHAR(50) NOT NULL,
    edad INT NOT NULL,
    sexo CHAR NOT NULL,
    municipio VARCHAR(20) NOT NULL,
    contrasenha VARCHAR(20) NOT NULL,
    nomUsu VARCHAR(50) NOT NULL,
    telefono VARCHAR(11),
    fecha_creacion DATE NOT NULL,
    CONSTRAINT PK_id_usuario PRIMARY KEY (id_usuario),
    constraint sexo_ck check (sexo in ('M', 'F')),
    CONSTRAINT municipiousu_ck CHECK (municipio IN (
    'achi',
    'altosrosario',
    'arenal',
    'arjona',
    'arroyohondo',
    'barrancoloba',
    'bocachica',
    'calamar',
    'cantagallo',
    'cartagena',
    'cicuco',
    'clemencia',
    'cordoba',
    'carmen',
    'elpenon',
    'hatilloloba',
    'magangue',
    'margarita',
    'marialbaja',
    'mompox',
    'montecristo',
    'morales',
    'norosí',
    'pinillos',
    'regidor',
    'rioviejo',
    'sancristobal',
    'sanestanislao',
    'sanfer',
    'sanja',
    'sanjuannepo',
    'sanmartinloba',
    'sanpablo',
    'santacatalina',
    'santarosalima',
    'santarosanorte',
    'simiti',
    'soplaviento',
    'talaigua',
    'tiquisio',
    'turbaco',
    'turbana',
    'villanueva',
    'zambrano'
))
);
 
CREATE TABLE deporte (
    id_deporte VARCHAR(50) NOT NULL,
    nomDepo VARCHAR(20) NOT NULL,
    CONSTRAINT PK_id_deporte PRIMARY KEY (id_deporte)
);
 
CREATE TABLE zona (
    id_zona VARCHAR(20) NOT NULL,
    nomZona VARCHAR(20) NOT NULL,
    municipio VARCHAR(20) NOT NULL,
    CONSTRAINT PK_id_zona PRIMARY KEY (id_zona),
    CONSTRAINT municipiozon_ck CHECK (municipio IN (
    'achi',
    'altosrosario',
    'arenal',
    'arjona',
    'arroyohondo',
    'barrancoloba',
    'bocachica',
    'calamar',
    'cantagallo',
    'cartagena',
    'cicuco',
    'clemencia',
    'cordoba',
    'carmen',
    'elpenon',
    'hatilloloba',
    'magangue',
    'margarita',
    'marialbaja',
    'mompox',
    'montecristo',
    'morales',
    'norosí',
    'pinillos',
    'regidor',
    'rioviejo',
    'sancristobal',
    'sanestanislao',
    'sanfer',
    'sanja',
    'sanjuannepo',
    'sanmartinloba',
    'sanpablo',
    'santacatalina',
    'santarosalima',
    'santarosanorte',
    'simiti',
    'soplaviento',
    'talaigua',
    'tiquisio',
    'turbaco',
    'turbana',
    'villanueva',
    'zambrano'
))
);
 
CREATE TABLE instalacion (
    id_instalacion VARCHAR(6) NOT NULL,
    nomInst VARCHAR(50) NOT NULL,
    id_zona VARCHAR(20) NULL,
    CONSTRAINT PK_id_instalacion PRIMARY KEY (id_instalacion),
    CONSTRAINT instalacion_zona_FK FOREIGN KEY (id_zona) 
        REFERENCES zona(id_zona)
);

CREATE TABLE entrenador (
    id_entrenador VARCHAR(20) NOT NULL,
    anhos_exp INT,
    id_instalacion VARCHAR(20) NOT NULL,
    CONSTRAINT PK_id_entrenador PRIMARY KEY (id_entrenador),
    CONSTRAINT entrenador_instalacion_FK FOREIGN KEY (id_instalacion)
        REFERENCES instalacion(id_instalacion)
);

CREATE TABLE horarios (
    id_horario VARCHAR(20) NOT NULL,
    dias DATE NOT NULL,
    hora_ini TIME NOT NULL,
    hora_fin TIME NOT NULL,
    id_instalacion VARCHAR(20) NOT NULL,
    CONSTRAINT PK_id_horario PRIMARY KEY (id_horario),
    CONSTRAINT horarios_instalacion_FK FOREIGN KEY (id_instalacion)
        REFERENCES instalacion(id_instalacion)
);

CREATE TABLE equipo (
    id_equipo VARCHAR(20) NOT NULL,
    nomEqui VARCHAR(50) NOT NULL,
    cant_int INT NOT NULL,
    cat_gen CHAR NOT NULL,
    cat_edad INT NOT NULL,
    id_deporte VARCHAR(50) NOT NULL,
    CONSTRAINT PK_id_equipo PRIMARY KEY (id_equipo),
    CONSTRAINT equipo_deporte FOREIGN KEY (id_deporte)
        REFERENCES deporte(id_deporte),
    CONSTRAINT cat_gen_ck CHECK (cat_gen IN ('M' , 'F'))
);

CREATE TABLE publicacion (
    id_publi VARCHAR(20) NOT NULL,
    tipo VARCHAR(10) NOT NULL,
    titulo TEXT NOT NULL,
    ruta_img VARCHAR(100),
    contenido TEXT,
    fecha_publi DATETIME NOT NULL,
    id_usuario VARCHAR(50),
    id_equipo VARCHAR(20),
    CONSTRAINT PK_id_publi PRIMARY KEY (id_publi),
    CONSTRAINT publicacion_usuario_FK FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario),
    CONSTRAINT publicacion_equipo_FK FOREIGN KEY (id_equipo)
        REFERENCES equipo(id_equipo)
);

CREATE TABLE evento (
    id_evento VARCHAR(20) NOT NULL,
    nomEve VARCHAR(20) NOT NULL,
    fecha_ini DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    descripcion TEXT NOT NULL,
    id_deporte VARCHAR(50) NOT NULL,
    id_instalacion VARCHAR(20) NOT NULL,
    id_usuario VARCHAR(50) NOT NULL,
    CONSTRAINT PK_id_evento PRIMARY KEY (id_evento),
    CONSTRAINT evento_deporte_FK FOREIGN KEY (id_deporte)
        REFERENCES deporte(id_deporte),
    CONSTRAINT evento_instalacion_FK FOREIGN KEY (id_instalacion)
        REFERENCES instalacion(id_instalacion),
    CONSTRAINT evento_usuario_FK FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario)
);

CREATE TABLE reserva (
    id_reserva VARCHAR(20),
    fecha_resIni DATETIME NOT NULL,
    fecha_resFin DATETIME NOT NULL,
    id_usuario VARCHAR(50),
    id_equipo VARCHAR(20),
    id_instalacion VARCHAR(20) NOT NULL,
    id_horario VARCHAR(20) NOT NULL,
    CONSTRAINT id_reserva_PK PRIMARY KEY (id_reserva),
    CONSTRAINT reserva_usuario_FK FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario),
    CONSTRAINT reserva_equipo_FK FOREIGN KEY (id_equipo)
        REFERENCES equipo(id_equipo),
    CONSTRAINT reserva_instalacion_FK FOREIGN KEY (id_instalacion)
        REFERENCES instalacion(id_instalacion),
    CONSTRAINT reserva_horario_FK FOREIGN KEY (id_horario)
        REFERENCES horarios(id_horario)
);

CREATE TABLE inscripcion (
    id_inscripcion VARCHAR(20) NOT NULL,
    id_equipo VARCHAR(20) NOT NULL,
    id_evento VARCHAR(20) NOT NULL,
    CONSTRAINT PK_id_inscripcion PRIMARY KEY (id_inscripcion),
    CONSTRAINT inscripcion_equipo_FK FOREIGN KEY (id_equipo)
        REFERENCES equipo(id_equipo),
    CONSTRAINT inscripcion_evento_FK FOREIGN KEY (id_evento)
        REFERENCES evento(id_evento)
);

CREATE TABLE integrante_equipo (
    rol_equipo VARCHAR(30) NOT NULL,
    id_usuario VARCHAR(50) NOT NULL,
    id_equipo VARCHAR(20) NOT NULL,
    CONSTRAINT usuario_equipo_FK FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario),
    CONSTRAINT equipo_usuario_FK FOREIGN KEY (id_equipo)
        REFERENCES equipo(id_equipo)
);

CREATE TABLE usuario_deporte (
    id_usuario VARCHAR(50) NOT NULL,
    id_deporte VARCHAR(50) NOT NULL,
    CONSTRAINT usuario_deporte_FK FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario),
    CONSTRAINT deporte_usuario_FK FOREIGN KEY (id_deporte)
        REFERENCES deporte(id_deporte)
);

CREATE TABLE entrenador_deporte (
    id_entrenador VARCHAR(20) NOT NULL,
    id_deporte VARCHAR(50) NOT NULL,
    CONSTRAINT entrenador_deporte_FK FOREIGN KEY (id_entrenador)
        REFERENCES entrenador(id_entrenador),
    CONSTRAINT deporte_entrenador_FK FOREIGN KEY (id_deporte)
        REFERENCES deporte(id_deporte)
);

CREATE TABLE deporte_instalacion (
    id_deporte VARCHAR(50) NOT NULL,
    id_instalacion VARCHAR(20) NOT NULL,
    CONSTRAINT deporte_instalacion_FK FOREIGN KEY (id_deporte)
        REFERENCES deporte(id_deporte),
    CONSTRAINT instalacion_deporte_FK FOREIGN KEY (id_instalacion)
        REFERENCES instalacion(id_instalacion)
);