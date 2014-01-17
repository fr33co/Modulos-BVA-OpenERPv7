# -*- coding: utf-8 -*-

import time
import random
from time import gmtime, strftime
from openerp.osv import osv, fields
from datetime import datetime, timedelta

#Clase Solicitud de reparacion de Canaima
class Solicitud_Canaima(osv.Model):
	_name = "solicitud"
	_order = 'c_solicitud'
	_rec_name = 'c_solicitud'

	_columns = {
		'serial' : fields.char(string="Serial", required=True),
		'modelo' : fields.char(string="Modelo", size=25, required=True),
		'estado' : fields.char(string="Estado Solicitud", readonly=True),
		'nombre' : fields.char(string="Nombre", size=25, required=True),
		'cedula' : fields.char(string="Cédula", size=8, required=True),
		'apellido' : fields.char(string="Apellido", size=25, required=True),
		'escuela' : fields.char(string="Escuela", size=50, required=True),
		'municipio' : fields.related('parroquia','municipio', type ='many2one', relation ='municipio', string = 'Municipio', required=True),
		#'municipio' : fields.many2one('municipio', 'Municipios', required=True),
		#'parroquia' : fields.char(string="Parroquia", size=40),
		'parroquia' : fields.many2one('parroquia', 'Parroquias', required=True),
		'direccion_i' : fields.text(string="Dirección Escuela"),
		'direccion_r' : fields.text(string="Dirección"),
		'nombre_r' : fields.char(string="Nombre Representante", size=25, required=True),
		'apellido_r' : fields.char(string="Apellido Representante", size=25, required=True),
		'telefono' : fields.char(string="Teléfono", size=11),
		'descripcion' : fields.text(string="Descripción del Problema"),
		'c_solicitud' : fields.char(string="Código", size=8, readonly=True, required=True),
		'f_solicitud': fields.char('Fecha de Solicitud', readonly=True,  required=True),
		'f_entrega': fields.date('Fecha de Entrega',  required=True),
		'canaimita' : fields.boolean('Canaimita'),
		'cargador' : fields.boolean('Cargador'),
		'bateria' : fields.boolean('Bateria'),
		'caja' : fields.boolean('Caja'),
		'contrato' : fields.boolean('Contrato'),
		
	}
	
	def _get_last_id(self, cr, uid, ids, context = None):

                sfl_id       = self.pool.get('solicitud')
                srch_id      = sfl_id.search(cr,uid,[])
                rd_id        = sfl_id.read(cr, uid, srch_id, context=context)
                if rd_id:
                    id_documento = rd_id[-1]['c_solicitud']
                    c_solicitud = id_documento[2:]
                    last_id      = c_solicitud.lstrip('0')
                    str_number   = str(int(last_id) + 1)
                    last_id      = str_number.rjust(5,'0')
                    codigo      = last_id
                else :
                    str_number = '1'
                    last_id      = str_number.rjust(5,'0')
                    codigo      = last_id
                return codigo

	_defaults = {
        'f_solicitud': lambda *a: time.strftime("%d-%m-%Y"),
        'c_solicitud' : _get_last_id
    }        

	# def onchange_fh_entrega(self, cr, uid, ids, f_entrega, context=None):
			 
	# 		res = {}
	# 		mensaje = {}
			        
	# 		now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
	# 		valores = {'f_entrega' : now}
	# 		if f_entrega != None:
	# 			if f_entrega < now:
	# 				mensaje = {'title': "Cuidado: Error!",
	# 						'message' : "No puede seleccionar como fecha de entrega dias anterioes a hoy",
	# 				}
					
	# 				valores = {'f_entrega' : None}
	# 			else:
	# 				valores = {'f_entrega' : f_entrega}

	# 		res.update(valores)
	# 		return {'value' : res, 'warning' : mensaje}
