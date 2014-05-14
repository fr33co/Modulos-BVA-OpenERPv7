# -*- coding: utf-8 -*-

import time
import random
from time import gmtime, strftime
from openerp.osv import osv, fields
from datetime import datetime, timedelta
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring #Necesario para la generación del .xsl
import netsvc
import tools
import logging
import xlwt
from xlwt import Workbook
from xlwt import Font
from xlwt import XFStyle
from xlwt import Borders
import os
import math
import re
import unicodedata
import base64 #Necesario para la generación del .xls

# Clase Solicitud de reparacion de Canaima
class solicitud_soporte(osv.Model):

    #  Nombre del objeto
    _name = "solicitud.soporte"

    #  Ordenar por codigo de solicitud y de ser llamado por otro  objeto muestre codigo de solicitud
    _order = 'c_solicitud'
    _rec_name = 'c_solicitud'

    # Acciones de cada uno de los botones de la barra de estado de solicitud
    def action_atendiendo(self, cr, uid, ids, context = None):
        return self.write(cr, uid, ids, {'status':'Atendiendo'}, context=context)

    def action_remitir(self, cr, uid, ids, context = None):
        return self.write(cr, uid, ids, {'status':'Remitir'}, context=context)

    def action_confirmado(self, cr, uid, ids, context = None):
        return self.write(cr, uid, ids, {'status':'Reparada'}, context=context)

    def action_listo(self, cr, uid, ids, context = None):
        return self.write(cr, uid, ids, {'status':'Entregada'}, context=context)

    def action_devuelta(self, cr, uid, ids, context = None):
        return self.write(cr, uid, ids, {'status':'Devuelta'}, context=context)

    """
    Metodo que genera el codigo se solicitud donde se busca el ultimo valor encontrado en la BD
    y se le suma 1.
    """
    def _get_last_id(self, cr, uid, ids, context = None):

        sfl_id       = self.pool.get('solicitud.soporte')
        srch_id      = sfl_id.search(cr,uid,[])
        rd_id        = sfl_id.read(cr, uid, srch_id, context=context)
        if rd_id:
            id_documento = rd_id[-1]['c_solicitud']
            c_solicitud = id_documento[3:]
            last_id      = c_solicitud.lstrip('0')
            str_number   = str(int(last_id) + 1)
            last_id      = str_number.rjust(6,'0')
            codigo      = 'SSC'+last_id
        else :
            str_number = '1'
            last_id      = str_number.rjust(6,'0')
            codigo      = 'SSC'+last_id
        return codigo
	
    """
    Funcion para eliminar las tildes de algun texto utilizando el modulo unicodedata.
    """
    def elimina_tildes(self, s):
    
        return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
	
    """
    Metodo con el cual generamos archivo .xls, configurando el estilo de las filas, como su fuente 
    tamaño alineacion entre otras cosas.
    """

    def generar_xsl(self, cr, uid, ids, context=None):

	header_style = XFStyle()
	borders = Borders()
	borders.left = 1
	borders.right = 1
	borders.top = 1
	borders.bottom = 1
	header_style.borders = borders
	first_book = Workbook()
	

	##########################################################################################
				# Estrutura principal del xsl (Encabezado)
	##########################################################################################
	style0 = xlwt.easyxf('font: name Arial, colour black, bold on') #Estilo de fuente negrita
	style1 = xlwt.easyxf('align: horiz center') #Estilo alinear al centro centrado
	ws1 = first_book.add_sheet('first_sheet', cell_overwrite_ok=True)
	ws1.write_merge(0, 0, 0, 8,) #Numero de columnas que se expandera el encabezado
	ws1.row(0).height = 300 #Grosor de la fila del encabezado
	#Declaramos los encabezados de las columnas asi:
	#"FilaN, ColumnaN, 'Nombre de la columna', estilo_columna"
	ws1.write(0, 0, 'LISTADO DE SOLICITUDES', style0)
	ws1.write(1, 0, 'Codigo de Solicitud', style0)
	ws1.write(1, 1, 'Modelo', style0)
	ws1.write(1, 2, 'Serial', style0)
	ws1.write(1, 3, 'Fecha de Solicitud', style0)
	ws1.write(1, 4, 'Cedula', style0)
	ws1.write(1, 5, 'Nombre', style0)
	ws1.write(1, 6, 'Apellido', style0)
	ws1.write(1, 7, 'Status', style0)
	ws1.write(1, 8, 'Registrado', style0)


	get_gc = self.pool.get('solicitud.soporte') # Objeto 
	search_repar = get_gc.search(cr, uid, [], context=None) # Se busca Todo
	r_canaimas = get_gc.read(cr,uid,search_repar,context=context) # Se refleja el resultado
	 
	i = 0
	for x in r_canaimas: # Bloque para la iteracion del objeto
		user_r = x['user_register'] #Como son camos many2one trae informacion que no necesitamos
		usuario = user_r[1]   #por eso declaramos una variable que muestre el dato en la posicion que necesitamos.
		mod = x['modelo'] 
		modelo = mod[1]
		nom = x['nombre_r'].upper()
		nombre = self.elimina_tildes(nom)
		ape = x['apellido_r'].upper()
		apellido = self.elimina_tildes(ape)
		 
		#Asociamos cada columna a un campo de la base de datos				
		ws1.write(i+2, 0, str(x['c_solicitud'])) 
		ws1.write(i+2, 1, modelo)
		ws1.write(i+2, 2, str(x['serial']))
		ws1.write(i+2, 3, str(x['f_solicitud']))
		ws1.write(i+2, 4, str(x['cedula']))
		ws1.write(i+2, 5, nombre)
		ws1.write(i+2, 6, apellido)
		ws1.write(i+2, 7, str(x['status']))
		ws1.write(i+2, 8, usuario)

		i = i + 1 # Acumulador de la data

	# Variables de tiempo (dia, mes, año) para que cada vez que 
	# se genere un reporte, al nombre se le adiera la fecha del día.
	dia = time.strftime('%d')
	mes = time.strftime('%m')
	year = time.strftime('%Y')
	fecha = dia+"-"+mes+"-"+year #Variable que concatena el dia la fecha y el año
	nom = 'Solicitudes Atendidas '+fecha+'.xls' #C
	
	first_book.save('openerp/addons/gestion_canaimas/reporte/'+nom)
	f = open('openerp/addons/gestion_canaimas/reporte/'+nom)
	
	r_archivo = self.pool.get('reportes.canaimas').create(cr, uid, {
	    'name' : nom,
	    'res_name' : nom,
	    'datas' : base64.encodestring(f.read()),
	    'datas_fname' : nom,
	    'res_model' : 'solicitud.soporte',
	    'gerencia' : 'Desarrollo Social',
	    },context=context)
	
	return r_archivo

    _columns = {
        'c_solicitud' : fields.char(string="Código de Solicitud", size=255, readonly=True, required=True),
        'user_register': fields.many2one('res.users', 'Registrado por:', readonly=True),
        'f_solicitud': fields.char('Fecha de Solicitud', readonly=True, required=True),
        'f_entrega': fields.date('Fecha de Entrega', required=True),
        'modelo' : fields.many2one('solicitud.modelo', string="Modelo", required=True),
        'serial' : fields.char(string="Serial", required=True),
        'descripcion' : fields.text(string="Descripción del Problema", required=True),
        'canaimita' : fields.boolean('Portatil'),
        'cargador' : fields.boolean('Cargador'),
        'bateria' : fields.boolean('Bateria'),
        'caja' : fields.boolean('Caja'),
        'contrato' : fields.boolean('Contrato'),
        'otros' : fields.boolean('Otros'),
        'status': fields.selection((('Atendiendo','Atendiendo'),('Remitir','Remitir'), ('Reparada','Reparada'), ('Entregada','Entregada'),('Devuelta','Devuelta')),'Status', required=True, readonly=True),
        'nombre' : fields.char(string="Nombre", size=25, required=True),
        'apellido' : fields.char(string="Apellido", size=25, required=True),
        't_educ': fields.many2one('solicitud.tipo.edu', 'Tipo de Nivel', required=True),
        'grado' : fields.many2one('solicitud.grado', string="Grado de estudio", required=True),
        'escuela' : fields.char(string="Escuela", size=50, required=True),
        'pais' : fields.many2one('res.country', 'Pais', required=True),
        'estado' : fields.many2one('res.country.state', 'Estado', required=True),
        'municipio' : fields.many2one('res.country.municipality', 'Municipio', required=True),
        'parroquia' : fields.many2one('res.country.parish', 'Parroquia', required=True),
        'direccion_i' : fields.text(string="Dirección Escuela", required=True),
        'nombre_r' : fields.char(string="Nombre Representante", size=25, required=True),
        'apellido_r' : fields.char(string="Apellido Representante", size=25, required=True),
        'cedula' : fields.char(string="Cédula", size=10, required=True),
        'telefono' : fields.char(string="Teléfono 1", size=11, required=True),	
        'telefono2' : fields.char(string="Teléfono 2", size=11, required=False),    
        'correo' : fields.char(string="Correo Electronico", size=30),
        'pais_r' : fields.many2one('res.country', 'Pais', required=True),
        'estado_r' : fields.many2one('res.country.state', 'Estado', required=True),
        'municipio_r' : fields.many2one('res.country.municipality', 'Municipio', required=True),
        'parroquia_r' : fields.many2one('res.country.parish', 'Parroquia', required=True),
        'direccion_r' : fields.text(string="Dirección", required=True),
        'solucion' : fields.text(string="Solución", required=False, readonly=True),  
        #'grafico' : fields.function(_grafica_modelos, type='integer', string='Conteo por modelo', store=True),
        'grafico': fields.integer('Modelos', track_visibility='always'),
        'grafico_s': fields.integer('Modelos', track_visibility='always'),
        }
        
    """
    Por defecto declaramos: 
	-El formato del campo de fecha de solicitud por dia, mes y año
	-El estatus de la solicitud inicie como Atendiendo
	-El campo Registrado cargue el nombre del usuario logeado
	-El pais por defecto vamos a filtrar.
    """
        
    _defaults = {
        'f_solicitud': lambda *a: time.strftime("%d/%m/%Y"),
        'c_solicitud': _get_last_id,
        'status': 'Atendiendo',
        'pais': 240,
        'pais_r': 240,
        'user_register': lambda s, cr, uid, c: uid,
        'grafico': 1,
        'grafico_s': 1,
    }     


