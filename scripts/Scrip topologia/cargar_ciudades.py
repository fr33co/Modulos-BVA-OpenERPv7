#!/usr/bin/env python
# coding: utf-8

import xmlrpclib
import csv

username = 'admin' #the user
pwd = '123456' #the password of the user
dbname = 'topologia' #the database

# Get the uid
# Se tiene que indicar el puerto en la URL
cargar_ciudades = xmlrpclib.ServerProxy ('http://localhost:8069/xmlrpc/common')
uid = cargar_ciudades.login(dbname, username, pwd)

#replace localhost:8069 with the address of the server
ciudades = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')

#sql="TRUNCATE ciudades"

#borrar = ciudades.execute(dbname, uid, pwd, 'ciudades', 'truncate')


filename = "cargar_ciudades.csv"
reader = csv.reader(open(filename,"rb"))
for row in reader:
    ciudades_venezuela = {
    'estado':row[1].rstrip(),
    'ciudad':row[2].rstrip(),
    'codigo_c': row[3].rstrip(),
	}
    id_ciudad = ciudades.execute(dbname, uid, pwd, 'ciudades', 'create', ciudades_venezuela)
    print id_ciudad

print "Ciudades Cargados Satisfactoriamente"
