# -*- coding: utf-8 -*-
import time
import random
from time import gmtime, strftime
from openerp.osv import osv, fields
from datetime import datetime, timedelta

class organos_entes(osv.Model):

	_name = "organos.entes"
	_rec_name = 'nombre_ente'
	_order = 'nombre_ente'
	_columns = {
		'user_register': fields.many2one('res.users', 'Registrado por:', readonly=True),
		'f_solicitud': fields.char('Fecha de Elaboración:', readonly=True, required=True),
		'nombre_ente' : fields.char(string="Nombre del Organo/Ente/Institución", required=True),
		'siglas' : fields.char(string="Unidad de Medida", required=True),
		'correo' : fields.char(string="Cantidad", required=False),
		'tipo': fields.selection([('1','Órgano'), ('2','Ente'), ('3','Empresa'), ('4','Unidad de Apoyo')], string="Tipo de Institución"),
		'tipo_estructura': fields.selection([('1','Dirección Superior de Gobierno'), ('2','Poder Público'),
			('3','Ente Descentralizado'), ('4','Desconocido'), ('5','Ente Desconcentrado')], string="Tipo de Estructura"),
		#'tipo_estructura':fields.many2one('tipo.estructura', 'Tipo de Estructura', ondelete='cascade', select=False),
		'sector':fields.many2one('organos.sectores', 'Sector', ondelete='cascade', select=False),
		'nom_responsable' : fields.char(string="Nombre del Responsable", required=False),
		'cargo' : fields.char(string="Cargo", required=False),
		'telefono' : fields.char(string="Teléfono", size=11, required=False),
		'ci' : fields.char(string="C.I.", size=8, required=False),
		'direccion' : fields.char(string="Dirección", size=170, required=False),
	}
	_defaults = {
		'f_solicitud': lambda *a: time.strftime("%d/%m/%Y"),
		'user_register': lambda s, cr, uid, c: uid,
	}    