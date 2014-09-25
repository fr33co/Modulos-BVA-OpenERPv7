# -*- coding: utf-8 -*-
import class_pdf
import time
import base64
import random
import unicodedata
from time import gmtime, strftime
from openerp.osv import osv, fields
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from operator import itemgetter
from itertools import groupby
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
from openerp import netsvc
from openerp import tools
from openerp.tools import float_compare, DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)

from openerp.tools import mute_logger

class inventario_bva(osv.Model):

	_inherit = "stock.inventory"
	
	
	"""
	Metodo con el cual llamo al objeto "res.company" donde estan todos la informacion de la compañia
	o empresa, donde segun la compañia que selecciones me traera toda su direccion (Estado, Municipio
	Parroquia y direccion precisa)
	"""
	def on_change_direccion(self, cr, uid, ids, institucion, context=None):
		values = {}
		if not institucion:
			return values
		datos = self.pool.get('res.company').browse(cr, uid, institucion, context=context)
		est = datos.state_id.name
		mun = datos.municipality_id.name
		par = datos.parish_id.name
		values.update({
			'estado' : est,
			'municipio' : mun,
			'parroquia' : par,
			'direccion' : datos.street,
		})
		return {'value' : values}
	
	"""
	Metodo que heredo del modelo stock.inventory donde cada vez que hago un inventario y le doy click
	al boton confirmar inventario, genero un movimiento. Para que adicionalmente de la información que
	ya mandaba, agregue los campos: g, sg, s, estado, bva y v_total

	"""
	
	def action_confirm2(self, cr, uid, ids, context=None):
		""" Confirm the inventory and writes its finished date
		@return: True
		"""
		if context is None:
		    context = {}
		# to perform the correct inventory corrections we need analyze stock location by
		# location, never recursively, so we use a special context
		product_context = dict(context, compute_child=False)
	
		location_obj = self.pool.get('stock.location')
		for inv in self.browse(cr, uid, ids, context=context):
		    move_ids = []
		    for line in inv.inventory_line_id:
			pid = line.product_id.id
			product_context.update(uom=line.product_uom.id, to_date=inv.date, date=inv.date, prodlot_id=line.prod_lot_id.id)
			amount = location_obj._product_get(cr, uid, line.location_id.id, [pid], product_context)[pid]
			change = line.product_qty - amount
			lot_id = line.prod_lot_id.id
			if change:
			    location_id = line.product_id.property_stock_inventory.id
			    value = {
				'name': _('INV:') + (line.inventory_id.name or ''),
				'product_id': line.product_id.id,
				'product_uom': line.product_uom.id,
				'g' : line.g,
				'sg' : line.sg,
				's' : line.s,
				'estado' : line.estado,
				'bva' : line.nidentificacion,
				'v_total' : float(line.v_total),
				'prodlot_id': lot_id,
				'date': inv.date,
			    }
	
			    if change > 0:
				value.update( {
				    'product_qty': change,
				    'location_id': location_id,
				    'location_dest_id': line.location_id.id,
				})
			    else:
				value.update( {
				    'product_qty': -change,
				    'location_id': line.location_id.id,
				    'location_dest_id': location_id,
				})
			    move_ids.append(self._inventory_line_hook(cr, uid, line, value))
		    self.write(cr, uid, [inv.id], {'state': 'confirm', 'move_ids': [(6, 0, move_ids)]})
		    self.pool.get('stock.move').action_confirm(cr, uid, move_ids, context=context)
		return True
	
	
	"""
	Metodo con el cual genero el archivo .pdf el cual contiene el formato de inventario de bienes
	"""

	def generate_inventario(self, cr, uid, ids, context=None): # Generacion de inventario
		
		# Instancia de la clase heredada L es horizontal y P es vertical
		# format A4, A3 o letter que son los formatos de la hoja (oficio, carta, etc)

		pdf=class_pdf.PDF(orientation='L',unit='mm',format='letter') #HORIENTACION DE LA PAGINA
		
		#pdf.set_title(title)
		pdf.set_author('Marcel Arcuri')
		pdf.alias_nb_pages() # LLAMADA DE PAGINACION
		pdf.add_page() # AÑADE UNA NUEVA PAGINACION
		#pdf.set_font('Times','',10) # TAMANO Y TIPO DE LETRA DE LA FUENTE
		pdf.set_font('Arial','B',15)
		pdf.set_fill_color(157,188,201) # COLOR DE BORDE DE LA CELDA
		pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
		#pdf.set_margins(8,10,10) # MARGENES DEL DOCUMENTO
		#pdf.ln(20) # Saldo de linea
		# 10 y 50 eje x y y 200 dimencion
		#pdf.line(10, 40, 200, 40) Linea
		inven = self.browse(cr, uid, ids, context=context)
		#pdf.ln(5)
		fec = ""
		servi = ""
		estado = ""
		municipio = ""
		parroquia = ""
		direccion = ""
		for x in inven:
			#variables que contienen informacion del modelo para ser colocada en los encabezados
			#del formato

			ubi = acento(x.ubicacion.name)
			
			if x.fecha_rep == False:
				fec == ""
			else:
				fec = acento(x.fecha_rep)
			
			if x.servicio == False:
				servi == ""
			else:
				servi = acento(x.servicio)
				
			if x.estado == False:
				estado == ""
			else:
				estado = acento(x.estado)
			
			if x.municipio == False:
				municipio == ""
			else:
				municipio = acento(x.municipio)
			if x.parroquia == False:
				parroquia == ""
			else:
				parroquia = acento(x.parroquia)
				
			if x.direccion == False:
				direccion == ""
			else:
				direccion = acento(x.direccion)
			
			nombre = acento(x.name)
			
			#Encabezado principal
			
			pdf.set_fill_color(255,255,255)
			pdf.set_font('Arial','B',12)
			pdf.set_y(0)
			pdf.set_x(120)
			pdf.write(50,"Inventario de Bienes Muebles")
			pdf.ln(30)
			
			pdf.set_font('Arial','B',8)
			pdf.cell(186,5,"",'',0,'C',1)
			pdf.cell(75,5,"FORMULARIO BM-1",'',1,'R',1)
			
			
			pdf.set_fill_color(255,255,255)
			pdf.set_font('Arial','B',8)
			pdf.cell(211,5,"",'',0,'C',1)
			pdf.cell(50,5,'Hoja N°: '.decode("UTF-8")+str(pdf.page_no()),0,1,'R',1)
			
			pdf.set_fill_color(255,255,255)
			pdf.set_font('Arial','B',8)
			pdf.cell(211,5,"",'',0,'C',1)
			pdf.cell(50,5,"2. Servicio: "+servi,'',1,'R',1)
			
			pdf.ln(-18)
			pdf.set_font('Arial','B',8)
			pdf.write(30,"1. Entidad Propietaria: Gobierno del Estado Aragua")
			pdf.ln(5)
			pdf.write(30,"3. Unidad de Trabajo o Dependencia: "+ubi)
			pdf.ln(5)
			pdf.write(30,"4. Estado: "+estado)
			pdf.ln(5)
			pdf.write(30,"5. Municipio: "+municipio)
			pdf.ln(5)
			pdf.write(30,"6. Parroquia: "+parroquia)
			pdf.ln(5)
			pdf.write(30,"7. Dirección o Lugar: ".decode("UTF-8")+direccion)
			pdf.ln(5)
			pdf.write(30,"8. Fecha: "+fec)
			
			# Fila de la cabezera de la tabla

			pdf.set_y(75)
			pdf.cell(24,5,"Clasificacion",'LTBR',1,'C',1)
			pdf.cell(8,5,"G",'LTBR',0,'C',1)
			pdf.cell(8,5,"S/G",'LTBR',0,'C',1)
			pdf.cell(8,5,"S",'LTBR',0,'C',1)
			
			pdf.set_y(75)
			pdf.set_x(34)
			pdf.cell(20,10,"Cantidad",'LTBR',0,'C',1)
			
			
			pdf.set_y(75)
			pdf.set_x(54)
			pdf.cell(25,10,"N Identificación".decode("UTF-8"),'LTBR',0,'C',1)
			
			pdf.set_y(75)
			pdf.set_x(79)
			pdf.cell(20,10,"Status",'LTBR',0,'C',1)
			
			pdf.set_y(75)
			pdf.set_x(99)
			pdf.cell(115,10,"Nombre Y Descripción del Elemento".decode("UTF-8"),'LTBR',0,'C',1)
			
			pdf.set_y(75)
			pdf.set_x(210)
			pdf.cell(30,10,"Valor Unitario Bs.",'LTBR',0,'C',1)
			
			pdf.set_y(75)
			pdf.set_x(240)
			pdf.cell(30,10,"Valor Total Bs.",'LTBR',1,'C',1)
		
		
		# Fin Cabezera
		pdf.set_font('Times','',10) # TAMANO DE LA FUENTE
		
		#Llamado del modelo que contiene el One2may para poder usar sus datos
		data_ids = self.read(cr, uid, ids, context=context)[0]
		payslip_id = data_ids['inventory_line_id'] # Grupo de IDS

		alm = self.pool.get('stock.inventory.line') # Objeto 
		datos = alm.search(cr, uid, [('id','=',payslip_id)], context=None)
		bienes = alm.read(cr,uid,datos,context=context)
		
		j = 0
		k = 0
		m = 0
		suma = 0.0
		suma2 = 0.0
		t = 0.0
		for i in bienes:
			if not float(i['v_unitario']):
				i['v_unitario'] = 0.0
			else:
				i['v_unitario']
			
			if not float(i['v_total']):
				i['v_total'] = 0.0
			else:
				i['v_total']
			
			if i['estado'] == '1':
				esta = 'Bueno'
			else:
				esta = 'Malo'

				
			if j == 20:
				pdf.add_page()

				
				pdf.set_fill_color(255,255,255)
				pdf.set_font('Arial','B',12)
				pdf.set_y(0)
				pdf.set_x(120)
				pdf.write(50,"Inventario de Bienes Muebles")
				pdf.ln(30)
				
				
				pdf.set_fill_color(255,255,255)
				pdf.set_font('Arial','B',8)
				pdf.cell(186,5,"",'',0,'C',1)
				pdf.cell(75,5,"FORMULARIO BM-1",'',1,'R',1)
				
				pdf.set_fill_color(255,255,255)
				pdf.set_font('Arial','B',8)
				pdf.cell(211,5,"",'',0,'C',1)
				pdf.cell(50,5,'Hoja N°: '.decode("UTF-8")+str(pdf.page_no()),0,1,'R',1)
				
				pdf.set_fill_color(255,255,255)
				pdf.set_font('Arial','B',8)
				pdf.cell(211,5,"",'',0,'C',1)
				pdf.cell(50,5,"2. Servicio: "+servi,'',1,'R',1)

				pdf.ln(-18)
				pdf.set_font('Arial','B',8)
				pdf.write(30,"1. Entidad Propietaria: Gobierno del Estado Aragua")
				pdf.ln(5)
				pdf.write(30,"3. Unidad de Trabajo o Dependencia: "+ubi)
				pdf.ln(5)
				pdf.write(30,"4. Estado: Aragua")
				pdf.ln(5)
				pdf.write(30,"5. Municipio: Girardot")
				pdf.ln(5)
				pdf.write(30,"6. Parroquia: Madre Maria")
				pdf.ln(5)
				pdf.write(30,"7. Dirección o Lugar: Complejo Cultural Santos Michelena Av Sucre c/c Princicpal de Calicanto".decode("UTF-8"))
				pdf.ln(5)
				pdf.write(30,"8. Fecha: "+fec)
				
				# Fila de la cabezara de la tabla
				
				pdf.set_y(75)
				pdf.cell(24,5,"Clasificacion",'LTBR',1,'C',1)
				pdf.cell(8,5,"G",'LTBR',0,'C',1)
				pdf.cell(8,5,"S/G",'LTBR',0,'C',1)
				pdf.cell(8,5,"S",'LTBR',0,'C',1)
		
				pdf.set_y(75)
				pdf.set_x(34)
				pdf.cell(20,10,"Cantidad",'LTBR',0,'C',1)
				pdf.set_y(75)
				pdf.set_x(54)
				pdf.cell(25,10,"N Identificación".decode("UTF-8"),'LTBR',0,'C',1)
		
				pdf.set_y(75)
				pdf.set_x(79)
				pdf.cell(20,10,"Status",'LTBR',0,'C',1)
		
				pdf.set_y(75)
				pdf.set_x(99)
				pdf.cell(115,10,"Nombre Y Descripción del Elemento".decode("UTF-8"),'LTBR',0,'C',1)
		
				pdf.set_y(75)
				pdf.set_x(210)
				pdf.cell(30,10,"Valor Unitario Bs.",'LTBR',0,'C',1)
		
				pdf.set_y(75)
				pdf.set_x(240)
				pdf.cell(30,10,"Valor Total Bs.",'LTBR',1,'C',1)
				
				# Fin Cabezera
				j=0
			
			t += float(i['v_total'])
			item = len(bienes)
			# Filas que vienen de la BD
			cantidad = int(i['product_qty'])
			pdf.set_font('Arial','',8)
			pdf.cell(8,5,str(i['g']),'LTBR',0,'C',1)
			pdf.cell(8,5,str(i['sg']),'LTBR',0,'C',1)
			pdf.cell(8,5,str(i['s']),'LTBR',0,'C',1)
			pdf.cell(20,5,str(cantidad),'LTBR',0,'C',1)
			pdf.cell(25,5,str(i['nidentificacion']),'LTBR',0,'C',1)
			pdf.cell(20,5,esta,'LTBR',0,'C',1)
			pdf.cell(111,5,str(i['product_id'][1]).decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(30,5,addComa(str(i['v_unitario'])),'LTBR',0,'C',1)
			pdf.cell(30,5,addComa(str((i['v_total']))),'LTBR',1,'C',1)
			suma = float(i['v_total']) + suma
			suma2 = float(i['v_total']) + suma
			pdf.set_font('Times','',10) # TAMANO DE LA FUENTE


			if k == 19 : 
				pdf.set_font('Arial','B',8)
				pdf.cell(170,5,"",0,0,'C',0)
				pdf.cell(30,5,"Total en Bolivares",0,0,'C',0)
				pdf.cell(60,5,addComa(str(suma)),'LTBR',1,'R',0)
				k = 0
				suma = 0
			j = j+1
			k = k+1
			
			
		
		pdf.set_font('Arial','B',8)
		pdf.cell(170,5,"",0,0,'C',0)
		pdf.cell(30,5,"Total en Bolivares",0,0,'C',0)
		pdf.cell(60,5,addComa(str(suma)),'LTBR',1,'R',0)
		
		pdf.ln(5)
		pdf.set_font('Arial','B',8)
		pdf.cell(90,5,"",0,0,'C',0)
		pdf.cell(55,5,"Total de Bienes",'LTBR',0,'C',0)
		pdf.cell(55,5,str(item),'LTBR',0,'C',0)
		pdf.cell(60,5,"",0,1,'R',0)
		
		pdf.set_font('Arial','B',8)
		pdf.cell(90,5,"",0,0,'C',0)
		pdf.cell(55,5,"Total en Bolivares",'LTBR',0,'C',0)
		pdf.cell(55,5,addComa(str(t)),'LTBR',0,'C',0)
		pdf.cell(60,5,"",0,1,'R',0)



		
#nom = nombre+" "+str(fec)+'.pdf' #Nombre del archivo .pdf
		nom = "prueba.pdf"
		
		#pdf.output('/home/administrador/openerp70/modules/producto_bva/reporte/'+nom,'F')
		pdf.output('openerp/addons/bienes_nacionales/reportes/'+nom,'F')

		#archivo = open('/home/administrador/openerp70/modules/producto_bva/reporte/'+nom)
		archivo = open('openerp/addons/bienes_nacionales/reportes/'+nom)

		"""
		Mandamos el archivo al modelo de reportes, donde se iran almacenando
		"""
		#r_archivo = self.pool.get('reporte.documentos').create(cr, uid, {
		# 	'name' : nom,
		# 	'res_name' : nom,
		# 	'datas' : base64.encodestring(archivo.read()),
		# 	'datas_fname' : nom,
		# 	'res_model' : 'stock.inventory',
		#	'tipo_reporte': "Inventario de Bienes",
		#	},context=context)
		#
		#return r_archivo
	
	_columns = {
		'usuario_login': fields.many2one('res.users', 'Registrado por:', readonly=True),
		'ubicacion' : fields.many2one('stock.location', 'Área Solicitante', required=False),
		'fecha_rep': fields.char('Fecha del Inventario:'),
		'institucion' : fields.many2one('res.company', 'Institución o Empresa', required=False),
		'estado': fields.char('Estado:'),
		'municipio': fields.char('Municipio:'),
		'parroquia': fields.char('Parroquia:'),
		'direccion': fields.char('Dirección:'),
		'servicio': fields.char('Servicio:', required=False),	
	}

	_defaults = {
		'usuario_login': lambda s, cr, uid, c: uid,
		
	}
def acento(cadena):
	result = cadena.encode('UTF-8').decode('UTF-8')# INSTITUCION
	return result
inventario_bva()

def addComa( snum ):
	"Adicionar comas como separadores de miles a n. n debe ser de tipo string"
	s = snum;
	i = s.index('.') # Se busca la posición del punto decimal
	while i > 3:
	    i = i - 3
	    s = s[:i] +  '#' + s[i:]
	    
	n = s.replace(".", ",", 5);
	t = n.replace("#", ".", 5);
	return t

class inventario_bva2(osv.Model):

 	_inherit = "stock.inventory.line"
	
	"""
	Metodo que de a cuerdo al elemento seleccionado trae de BD toda la informacion
	que contiene. 
	"""
	
	def on_change_product_id(self, cr, uid, ids, location_id, product, uom=False, to_date=False):
		""" Changes UoM and name if product_id changes.
		@param location_id: Location id
		@param product: Changed product_id
		@param uom: UoM product
		@return:  Dictionary of changed values
		"""
		values = {}
		if not product:
		    return {'value': {'product_qty': 0.0, 'product_uom': False, 'prod_lot_id': False, 'g' : False, 'sg' : False,
					's' : False, 'estado' : False, 'nidentificacion' : False, 'v_unitario' : 0.0, 'v_total' : 0.0,}}
		obj_product = self.pool.get('product.product').browse(cr, uid, product)
		amount = self.pool.get('stock.location')._product_get(cr, uid, location_id, [product], {'uom': uom, 'to_date': to_date, 'compute_child': False})[product]
		uom = uom or obj_product.uom_id.id
		if obj_product.estado == '1':
			val = 'Bueno'
		else:
			val = 'Malo'
		print val
		values.update({
			'g' : obj_product.g,
			'sg' : obj_product.sg,
			's' : obj_product.s,
			'estado' : obj_product.estado,
			'nidentificacion' : obj_product.nidentificacion,
			'v_unitario' : obj_product.v_unitario,
			'v_total' : obj_product.v_total,
			'product_qty': amount,
			'product_uom': uom,
			'prod_lot_id': False,
		})
		return {'value': values}
	
	_columns = {

 		'g' : fields.char(string="G", required=False),
 		'sg' : fields.char(string="S/G", required=False),
 		's' : fields.char(string="S", required=False),
 		'nidentificacion' : fields.char(string="N de Identificacion", required=False),
		'estado' : fields.selection((('1','Bueno'), ('2','Malo')),'Status', required=False),
 		#'estado' : fields.char(string="Status", required=False),
 		'v_unitario' : fields.char(string="Valor Unitario Bs.", required=False),
 		'v_total' : fields.char(string="Valor Unitario Bs.", required=False),

 	}

class ubicacion_producto(osv.Model):

	"""
	Herencia del metodo de llenado de inventario, del wizar stock.fill.inventory con la finalidad
	de que aparte de traer los datos que busca por defecto, agregue otros requeridos.
	"""


	_inherit = "stock.fill.inventory"

	def llenar_inventario(self, cr, uid, ids, context=None):

		if context is None:
		    context = {}
	
		inventory_line_obj = self.pool.get('stock.inventory.line')
		location_obj = self.pool.get('stock.location')
		move_obj = self.pool.get('stock.move')
		uom_obj = self.pool.get('product.uom')
		if ids and len(ids):
		    ids = ids[0]
		else:
		     return {'type': 'ir.actions.act_window_close'}
		fill_inventory = self.browse(cr, uid, ids, context=context)
		res = {}
		res_location = {}
	
		if fill_inventory.recursive:
		    location_ids = location_obj.search(cr, uid, [('location_id',
				     'child_of', [fill_inventory.location_id.id])], order="id",
				     context=context)
		else:
		    location_ids = [fill_inventory.location_id.id]
	
		res = {}
		flag = False
	
		for location in location_ids:
		    datas = {}
		    res[location] = {}
		    move_ids = move_obj.search(cr, uid, ['|',('location_dest_id','=',location),('location_id','=',location),('state','=','done')], context=context)
		    #read_llenar  = move_obj.read(cr, uid, move_ids, context=None)
		    #print read_llenar['sg']
		    for move in move_obj.browse(cr, uid, move_ids, context=context):
			lot_id = move.prodlot_id.id
			prod_id = move.product_id.id
			print "Elemento"
			sub_grupo = move.sg
			sector = move.s
			grupo = move.g
			esta = move.estado
			codigo= move.bva
			bsf = move.v_total
			if move.location_dest_id.id != move.location_id.id:
			    if move.location_dest_id.id == location:
				qty = uom_obj._compute_qty(cr, uid, move.product_uom.id,move.product_qty, move.product_id.uom_id.id)
			    else:
				qty = -uom_obj._compute_qty(cr, uid, move.product_uom.id,move.product_qty, move.product_id.uom_id.id)
	
	
			    if datas.get((prod_id, lot_id)):
				qty += datas[(prod_id, lot_id)]['product_qty']
	
			    datas[(prod_id, lot_id)] = {
					'product_id': prod_id,
					'location_id': location,
					'product_qty': qty,
					'g' : grupo,
					'sg' : sub_grupo,
					's' : sector,
					'estado' : esta,
					'nidentificacion' : codigo,
					'v_total' : bsf,
					'product_uom': move.product_id.uom_id.id,
					'prod_lot_id': lot_id
				}
	
		    if datas:
			flag = True
			res[location] = datas
	
		if not flag:
		    raise osv.except_osv(_('Warning!'), _('No product in this location. Please select a location in the product form.'))
	
		for stock_move in res.values():
		    for stock_move_details in stock_move.values():
			stock_move_details.update({'inventory_id': context['active_ids'][0]})
			domain = []
			for field, value in stock_move_details.items():
			    if field == 'product_qty' and fill_inventory.set_stock_zero:
				 domain.append((field, 'in', [value,'0']))
				 continue
			    domain.append((field, '=', value))
	
			if fill_inventory.set_stock_zero:
			    stock_move_details.update({'product_qty': 0})
	
			line_ids = inventory_line_obj.search(cr, uid, domain, context=context)
	
			if not line_ids:
			    inventory_line_obj.create(cr, uid, stock_move_details, context=context)
	
		return {'type': 'ir.actions.act_window_close'}
    
	#stock_fill_inventory()
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: