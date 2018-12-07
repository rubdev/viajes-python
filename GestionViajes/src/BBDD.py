# -*- coding: utf-8 -*-

"""
    Archivo para la conexion con BD SQLITE
"""

import sys

try:
    import sqlite3
except:
    print("No existe SQLITE3")
    sys.exit(1)

class Conector:
    
    #constructor
    def __init__(self,nombre):
        print("Clase conector creada")
        self.cursor = sqlite3.connect(nombre)
        print("Creada conexion para BD:",nombre)
    
    #Devuelve conexion
    def dame_conexion(self):
        return self.cursor
    
    #Crea el esquema de la BD
    def crear_esquema(self,tipo):
        if tipo == 'reinicia':
            self.cursor.execute("DROP TABLE Venta")
            self.cursor.execute("DROP TABLE Cliente")
            self.cursor.execute("DROP TABLE Paquete")
            print("BORRO LAS TABLAS PORQUE HAS PULSADO REINICIAR BD")
        
        print("CREO LAS TABLAS DE NUEVO")
        self.cursor.execute("""
            CREATE TABLE Cliente (
            clienteID INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(50),
            apellidos VARCHAR(100),
            fechaNacimiento VARCHAR(10),
            dni VARCHAR(9),
            pasaporte VARCHAR(9),
            telefono VARCHAR(9),
            email VARCHAR(50),
            direccion VARCHAR(100)
        )
        """)
        
        self.cursor.execute("""
            CREATE TABLE Paquete (
            paqueteID INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(200),
            precio INTEGER,
            hospedaje VARCHAR(200),
            duracion VARCHAR(30),
            destino VARCHAR(200),
            transporte VARCHAR(200)
        )
        """)
        
        self.cursor.execute("""\
        CREATE TABLE Venta (
            ventaID INTEGER PRIMARY KEY AUTOINCREMENT,
            fechaVenta VARCHAR(10),
            fechaInicio VARCHAR(10),
            fechaFin VARCHAR(10),
            IdCli INTEGER,
            IdPaq INTEGER,
            CONSTRAINT fk_id_cli FOREIGN KEY (IdCli) REFERENCES Cliente(clienteID) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT fk_id_paq FOREIGN KEY (IdPaq) REFERENCES Paquete(paqueteID) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """)
        