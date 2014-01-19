#!/usr/bin/env python
# coding: utf-8

import xmlrpclib
import csv

username = 'admin' #the user
pwd = '123456' #the password of the user
dbname = 'Prueba5' #the database

# Get the uid
# Se tiene que indicar el puerto en la URL
conexion = xmlrpclib.ServerProxy ('http://localhost:8069/xmlrpc/common')
uid = conexion.login(dbname, username, pwd)

#replace localhost:8069 with the address of the server
up = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')

filename = "parroquias2.csv"
reader = csv.reader(open(filename,"rb"))
for row in reader:
    parroquias_aragua = {
    'municipio':row[0].rstrip(),
    'parroquia':row[1].rstrip(),

	}
    id_parroquia = up.execute(dbname, uid, pwd, 'parroquia', 'create', parroquias_aragua)
    print id_parroquia

print "Parroquias Cargados Satisfactoriamente"