# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from datetime import datetime, timedelta # Importacion del objeto datetime, forma para validar la fecha de inicio con la fecha final
from pygtk import require
import MySQLdb

class Configuracion(osv.Model):
	_order = "status"
	_rec_name = "status"
	_name="configuracion.caso"

	_columns = {
	'cod_estatus' : fields.integer(string="Código de Estátus", size=20, required=True),
	'status' : fields.char(string="Descripción del Estátus", size=256, required=True),
	}
	
	
        _sql_constraints = [
			('cod_estatus_unique','UNIQUE(cod_estatus)','Disculpe este Código ya existe...'),
			('status_unique','UNIQUE(status)','Disculpe este Estatus ya existe...'),
		]
     
