#!/usr/bin/env python
# coding: utf-8

import xmlrpclib
import csv

username = 'admin' #the user
pwd = '123456' #the password of the user
dbname = 'Prueba5' #the database

# Get the uid
# Se tiene que indicar el puerto en la URL
municipios = xmlrpclib.ServerProxy ('http://localhost:8069/xmlrpc/common')
uid = municipios.login(dbname, username, pwd)

#replace localhost:8069 with the address of the server
municipios = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')

filename = "municipio.csv"
reader = csv.reader(open(filename,"rb"))
for row in reader:
    municipios_aragua = {
    'municipio':row[0].rstrip(),

	}
    id_municipio = municipios.execute(dbname, uid, pwd, 'municipio', 'create', municipios_aragua)
    print id_municipio

print "Municipios Cargados Satisfactoriamente"