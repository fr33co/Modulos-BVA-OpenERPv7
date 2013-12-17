# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from datetime import datetime, timedelta # Importacion del objeto datetime, forma para validar la fecha de inicio con la fecha final
from pygtk import require
import MySQLdb

class Tipos(osv.Model):
	_order = "caso"
	_rec_name = "caso"
	_name="tipos.caso"

	_columns = {
	'cod_caso' : fields.integer(string="Código de Caso", size=20, required=True),
	'caso' : fields.char(string="Descripción del Caso", size=256, required=True),
	}
     
