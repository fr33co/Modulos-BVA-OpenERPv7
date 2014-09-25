# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import osv, fields

class Beneficiario(osv.Model):
	#~ _name = "tesoreria.beneficiario"
	#~ 
	#~ _order = "nombre"
	#~ 
	#~ _rec_name = "nombre"
	
	_inherit = "res.partner"

	_columns = {
		'beneficiario' : fields.boolean(string="Beneficiario",required=False),
		#~ 'nacionalidad' : fields.selection((('1','V'),('2','E')),"Nacionalidad", required = False),
		#~ 'tipo_benef' : fields.many2one("tesoreria.tipobeneficiario", "Tipo de Benef/Prov/Dpto", required = True),
		'cedula_rif': fields.char(string = "Cédula o Rif", size = 12, required = True, help="Indique la cedula o el rif"),
		#~ 'nombre' : fields.char(string="Nombre o Razón Social", required = True),
		#~ 'country_id' : fields.many2one("res.country", "País", required=True),
		#~ 'estado' : fields.many2one("res.country.state", "Estado", required = True, select="0"),
		#~ 'municipio' : fields.many2one("res.country.municipality", "Municipio", required = False, select="0"),
		#~ 'parroquia' : fields.many2one("res.country.parish", "Parroquia", required = False, select="0"),
		#~ 'direccion' : fields.char(string="Dirección", help="Ingrese la dirección", required = True),
		#~ 'telefono' : fields.char(string="Teléfono", size = 11, help="Ingrese el teléfono", required = True),
		#~ 'alquiler' : fields.boolean(string="Alquiler", required = False),
	}

	#NO BORRAR, ES UNA GUÍA...
	#~ _sql_constraints = [
	    #~ ('cedula_familiar_unique',#cedula_becado_unique
	     #~ 'UNIQUE(cedula_familiar)',#cedula_becado
	     #~ 'Disculpe el familiar ya existe'),#Disculpe el Registro ya existe
	#~ ]
	
	_defaults = {
		'country_id' : 240,
		'state_id' : 55,
	}


