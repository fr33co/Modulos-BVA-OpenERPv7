# -*- coding: utf-8 -*-
import time
from openerp.osv import osv, fields, orm
from datetime import datetime, timedelta
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp import tools

class almacen_bva(osv.Model):

	_name = "materiales.almacen"
	_order = 'descripcion'
	_rec_name = 'descripcion'

	"""
	Metodo que genera el codigo se solicitud donde se busca el ultimo valor encontrado en la BD
	y se le suma 1.
	"""

	def correlativo_interno_material(self, cr, uid, ids, context = None):

		correlativo_mat = ""        
			
		cr.execute("SELECT count(*) as num_materiales FROM materiales_almacen")
		num_materiales = cr.fetchone()[0]
			
		#anyo = time.strftime("%Y")
			
		correlativo_mat = "M-"+str(num_materiales+1).zfill(6)
				
		return correlativo_mat
	

	_columns = {
		'codigo' : fields.char(string="Código", required=False, readonly=True),
		'fecha': fields.char('Fecha:', readonly=True,  required=True),
		'user_register': fields.many2one('res.users', 'Registrado por:', readonly=True),
		't_materiales' : fields.selection((('1','Limpieza'), ('2','Oficina'), ('3','Servicios Generales'), ('4','Tecnológico')),'Tipo de Material', required=False),
		'unidad':fields.many2one('product.uom', 'Unidad de Medida',required=True),
		'descripcion' : fields.char(string="Descripción del Material", size=50, required=True),
	}
	
	#Restriccion para que la descripcion del Material sea unica y evitar duplicidad
	_sql_constraints = [
	('descripcion_unique','UNIQUE(descripcion)','Material ya registrado'),
	]
	
	"""
	Por Defecto:
		- El campo codigo genera un codigo unico que incrementa con cada registro.
		- El campo user_register muestra automaticamente el usuario logeado.
	"""
	_defaults = {
		'codigo': correlativo_interno_material,
		'user_register': lambda s, cr, uid, c: uid,
		'fecha': lambda *a: time.strftime("%d/%m/%Y"),
	}