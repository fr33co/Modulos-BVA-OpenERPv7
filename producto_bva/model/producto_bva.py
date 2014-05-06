# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class producto_bva(osv.Model):

	_inherit = "product.product"
	_columns = {
		'g' : fields.char(string="G", size=2, required=True),
		'sg' : fields.char(string="S/G", size=2, required=True),
		's' : fields.char(string="S", size=2, required=True),
		'estado' : fields.selection((('1','Bueno'), ('2','Malo')),'Status', required=True),
		'codigo':fields.many2one('codigos.bva', 'Código',required=True),
		#'codigo' : fields.selection((('BBV','BBV'), ('BVA','BVA'), ('BE','BE'), ('No se codifica','No se codifica')),'Código Bien Nacional', required=True),
		'numero' : fields.char(string="Número del Bien", size=20),
		'nombre_des' : fields.char(string="Nombre y Descripción del Elemento"),
		'union' : fields.char(string="Relación"),
		'nidentificacion' : fields.char(string="N de Identificacion", size=20),
		'v_unitario' : fields.float(string="Valor Unitario Bs.", size=20, required=True),
		'v_total' : fields.float(string="Valor Total Bs.", size=20, required=True),
		'serial' : fields.char(string="Serial", required=False),
		'donacion' : fields.boolean("Donación"),
		'incorporacion':fields.many2one('procesos.incorporaciones', 'Incorporación por', required=False),
	}

	#Restriccion para que la descripcion del Material sea unica y evitar duplicidad
	_sql_constraints = [
		('descripcion_unique','UNIQUE(union)','Elemento ya registrado con el mismo nombre, serial y código de bien'),
	]
	
	_defaults = {
		'sale_ok': False,
		'type': 'product',
		}

	"""    
	Este metodo valida que de ser seleccionado en el codigo del bien el parametro "No se codifica"
	automaticamente envia al campo invisible (nidentificacion) el parametro "No se codifica" 
	para se mostrado en el registro
	"""
	
	def on_change_codigo(self, cr, uid, ids, codigo, context=None):
		values = {}
		datos = self.pool.get('codigos.bva')
		variable = datos.browse(cr, uid, codigo, context=context)
		rd_id        = datos.read(cr, uid, variable.id, ['codigo'], context=context)
		c_bien = rd_id['codigo']

		if c_bien == 'No se codifica': 
			codigo_id2 = 'No se codifica'
		else: 
		 	codigo_id2 = ''

		values.update({'nidentificacion' : codigo_id2,})
		return {'value' : values}

	"""
	Metodo ubicado en el campo status a modo que una vez que se seleccione el status del bien
	automaticamente genere la concatenación de los campos nombre_des codigo y numero en un solo
	campo invisible el cual se somete a un sqlcontraing a modo de evitar duplicidad de los 
	registros. A su vez une el campo codigo y numero para asi generar el codigo de bien Nacional
	completo.
	"""


	def on_change_identificacion(self, cr, uid, ids, codigo, numero, name, nombre_des, serial, context=None):
		values = {}
		serial2 = ''
		datos = self.pool.get('codigos.bva')
		variable = datos.browse(cr, uid, codigo, context=context)
		rd_id        = datos.read(cr, uid, variable.id, ['codigo'], context=context)
		c_bien = rd_id['codigo']
		
		if serial == False:
			serial = serial2
		if not numero:
			return values
		
		codigo_id = str(c_bien)+'-'+str(numero)
		relacion =  str(nombre_des)+' '+str(serial)+'-'+str(c_bien)+'-'+str(numero)
		n_descrip = str(nombre_des)+' '+str(serial)
		values.update({'nidentificacion' : codigo_id, 'union' : relacion, 'name' : n_descrip,})
		return {'value' : values}

	"""
	Metodo que dependiendo de la categoria del producto que selecciones trae toda la infomacion
	de la clasificacion del mismo.
	"""

	def on_change_clasificacion(self, cr, uid, ids, categ_id, context=None):
		values = {}
		if not categ_id:
			return values
		datos = self.pool.get('product.category').browse(cr, uid, categ_id, context=context)
		values.update({
			'g' : datos.g,
			'sg' : datos.sg,
			's' : datos.s,
		})
		return {'value' : values}  