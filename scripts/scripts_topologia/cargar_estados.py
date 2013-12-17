#!/usr/bin/env python
# coding: utf-8

import xmlrpclib
import csv

username = 'admin' #the user
pwd = '123456' #the password of the user
dbname = 'topologia' #the database

# Get the uid
# Se tiene que indicar el puerto en la URL
cargar_estados = xmlrpclib.ServerProxy ('http://localhost:8069/xmlrpc/common')
uid = cargar_estados.login(dbname, username, pwd)

#replace localhost:8069 with the address of the server
estados = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')

#sql="TRUNCATE estados"

#borrar = estados.execute(dbname, uid, pwd, 'estados', 'truncate')


filename = "cargar_estados.csv"
reader = csv.reader(open(filename,"rb"))
for row in reader:
    estados_venezuela = {
    'codigo_e': row[1].rstrip(),
    'estado':row[2].rstrip(),
	}
    id_estado = estados.execute(dbname, uid, pwd, 'estados', 'create', estados_venezuela)
    print id_estado

print "Estados Cargados Satisfactoriamente"
