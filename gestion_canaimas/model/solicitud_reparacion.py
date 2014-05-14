# -*- coding: utf-8 -*-
import time
import urllib2, urllib
from datetime import datetime
from dateutil import relativedelta

from openerp.osv import fields, osv
from openerp.tools.translate import _
import base64 #Necesario para la generación del .txt
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

class solicitud_reparacion(osv.Model):

    # Nombre de el Objeto
    _name = "solicitud.reparacion"

    # Se Ordena por Codigo de solicitud  
    _order = 'c_solicitud'
   # _rec_name = ''

    """
    Metodo que trae la informacion de las solicitud de soporte de la clase solicitud_soporte
    al formulario de solicitud de reparación.
    """
    def on_change_datos(self, cr, uid, ids, c_solicitud, context=None):
        values = {}
        if not c_solicitud:
            return values
        datos = self.pool.get('solicitud.soporte').browse(cr, uid, c_solicitud, context=context)
        entrega = datos.f_entrega.split("-")
        fecha2= entrega[2]+"/"+entrega[1]+"/"+entrega[0]
        values.update({
            'serial' : datos.serial,
            'modelo' : datos.modelo.modelo,
            'status_ss' : datos.status,
            'descripcion' : datos.descripcion,
            'f_solicitud': datos.f_solicitud,
            'f_entrega': fecha2,
        })
        return {'value' : values}

    """
    Metodo que al cambiar el estado de la solicitud en el objeto solicitud_reparacion cambia
    automaticamente en el objeto solicitud_soporte y tambien envia la Solucion o diagnostico 
    del Problema.
    """
    def actualizar_status(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=None)
        obj_estado = self.pool.get('solicitud.soporte')
        estado_s = self.browse(cr, uid, ids)[0]
        for r2 in obj:
            rd_estado = obj_estado.read(cr, uid, r2.c_solicitud.id, context=context)
            resultado = rd_estado['c_solicitud']
            status2  = estado_s.status
            solucionc = estado_s.solucion
            tecnicos = estado_s.tecnico
            cr.execute("UPDATE solicitud_soporte SET status=%s, solucion=%s WHERE c_solicitud=%s;", (status2, solucionc, resultado,))
        return True
	
	"""
	Metodo con el cual generamos archivo .xls, configurando el estilo de las filas como su fuente 
	tamaño alineacion entre otras cosas.
	"""

    def generate_xsl_slip(self, cr, uid, ids, context=None):

	header_style = XFStyle()
	borders = Borders()
	borders.left = 1
	borders.right = 1
	borders.top = 1
	borders.bottom = 1
	header_style.borders = borders
	first_book = Workbook()
	

	#################################################################
				# Estrutura principal del xsl (Encabezado)
	#################################################################
	style0 = xlwt.easyxf('font: name Times New Roman, colour black, bold on') #Estilo de fuente negrita
	style1 = xlwt.easyxf('align: horiz center') #Estilo alinear al centro centrado
	ws1 = first_book.add_sheet('first_sheet', cell_overwrite_ok=True)
	ws1.write_merge(0, 0, 0, 7,) #Numero de columnas que se expandera el encabezado
	ws1.row(0).height = 300 #Grosor de la fila del encabezado
	#Declaramos los encabezados de las columnas asi:
	#"FilaN, ColumnaN, 'Nombre de la columna', estilo_columna"
	ws1.write(0, 0, 'LISTADO DE REPARACIONES', style0)
	ws1.write(1, 0, 'Codigo de Solicitud', style0)
	ws1.write(1, 1, 'Modelo', style0)
	ws1.write(1, 2, 'Serial', style0)
	ws1.write(1, 3, 'Fecha de Solicitud', style0)
	ws1.write(1, 4, 'Estado de Solicitud', style0)
	ws1.write(1, 5, 'Hardware', style0)
	ws1.write(1, 6, 'Software', style0)
	ws1.write(1, 7, 'Tecnico', style0)


	get_gc = self.pool.get('solicitud.reparacion') # Objeto 
	search_repar = get_gc.search(cr, uid, [], context=None) # Se busqa Todo
	r_canaimas = get_gc.read(cr,uid,search_repar,context=context) # Se refleja el resultado
	 
	i = 0
	for x in r_canaimas: # Bloque para la iteracion del objeto
		a = x['c_solicitud'] #Como son camos many2one trae informacion que no necesitamos
		n_solicitud = a[1]   #por eso declaramos una variable que muestre el dato en la posicion que necesitamos.
		b = x['tecnico'] 
		n_tecnico = b[1]
		if x['hardware'] == True:
			har = 'X'
		else:
			har = ''
		if x['software'] == True:
			sof = 'X'
		else:
			sof = ''
		
		#Asociamos cada columna a un campo de la base de datos				
		ws1.write(i+2, 0, n_solicitud) 
		ws1.write(i+2, 1, str(x['modelo']))
		ws1.write(i+2, 2, str(x['serial']))
		ws1.write(i+2, 3, str(x['f_solicitud']))
		ws1.write(i+2, 4, str(x['status']))
		ws1.write(i+2, 5, har, style1)
		ws1.write(i+2, 6, sof, style1)
		ws1.write(i+2, 7, n_tecnico)


		i = i + 1 # Acumulador de la data

	# Variables de tiempo (dia, mes, año) para que cada vez que 
	# se genere un reporte, al nombre se le adiera la fecha del día.
	dia = time.strftime('%d')
	mes = time.strftime('%m')
	year = time.strftime('%Y')
	fecha = dia+"-"+mes+"-"+year #Variable que concatena el dia la fecha y el año
	nom = 'Reparaciones totales '+fecha+'.xls' #C
	
	first_book.save('openerp/addons/gestion_canaimas/reporte/'+nom)
	f = open('openerp/addons/gestion_canaimas/reporte/'+nom)

	r_archivo = self.pool.get('reportes.canaimas').create(cr, uid, {
	    'name' : nom,
	    'res_name' : nom,
	    'datas' : base64.encodestring(f.read()),
	    'datas_fname' : nom,
	    'res_model' : 'solicitud.reparacion',
	    'gerencia' : 'Técnologia',
	    },context=context)
	
	return r_archivo
    _columns = {
        'c_solicitud' : fields.many2one('solicitud.soporte', 'Código de Solicitud', domain="[('status','ilike','Atendiendo')]", required=True),
        'f_solicitud': fields.char('Fecha de Solicitud', readonly=False),
        'f_entrega': fields.char('Fecha de Entrega', readonly=False),
        'serial' : fields.char(string="Serial", readonly=False),
        'modelo' : fields.char(string="Modelo", readonly=False),
        'status_ss' : fields.char(string="Status de la solicitud", readonly=False),
        'descripcion' : fields.text(string="Descripción del Problema", readonly=False),
        'tecnico' : fields.many2one('res.users', 'Técnico', required=False, readonly=False),
        'solucion' : fields.text(string="Solución", required=True),        
        'hardware' : fields.boolean('Hardware'),
        'software' : fields.boolean('Software'),
        'status': fields.selection([('Reparada','Reparada'), ('Remitir','Remitir')], string="Estado de Solicitud"),
        }
    
    # Se declara que por defecto el campo Técnico cargue el nombre del usuario logeado
    _defaults = {
        'tecnico': lambda s, cr, uid, c: uid,
    }       


