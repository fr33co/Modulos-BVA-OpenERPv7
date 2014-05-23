# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
import class_pdf
import time
import base64
from time import gmtime, strftime
from datetime import datetime, timedelta

class inventario_bva(osv.Model):

	_inherit = "stock.inventory"

	def generate_inventario(self, cr, uid, ids, context=None): # Generacion de inventario
		
		# Instancia de la clase heredada L es horizontal y P es vertical

		pdf=class_pdf.PDF(orientation='L',unit='mm',format='A4') #HORIENTACION DE LA PAGINA
		
		#pdf.set_title(title)
		pdf.set_author('Marcel Arcuri')
		pdf.alias_nb_pages() # LLAMADA DE PAGINACION
		pdf.add_page() # AÑADE UNA NUEVA PAGINACION
		#pdf.set_font('Times','',10) # TAMANO DE LA FUENTE
		pdf.set_font('Arial','B',15)
		pdf.set_fill_color(157,188,201) # COLOR DE BOLDE DE LA CELDA
		pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
		#pdf.set_margins(8,10,10) # MARGENE DEL DOCUMENTO
		#pdf.ln(20) # Saldo de linea
		# 10 y 50 eje x y y 200 dimencion
		#pdf.line(10, 40, 200, 40) Linea
		pdf.ln(10)
		pdf.set_fill_color(255,255,255)
		pdf.set_font('Arial','B',12)
		pdf.cell(100,5,"",'',0,'C',1)
		pdf.cell(80,5,"Inventario de Bienes Muebles",'',0,'C',1)
		pdf.cell(75,5,"",'',1,'C',1)
		
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
		pdf.cell(50,5,"2. Servicio: ",'',1,'R',1)
		
		pdf.ln(-18)
		pdf.set_font('Arial','B',8)
		pdf.write(30,"1. Entidad Propietaria: Gobierno del Estado Aragua")
		pdf.ln(5)
		pdf.write(30,"3. Unidad de Trabajo o Dependencia")
		pdf.ln(5)
		pdf.write(30,"4. Estado: Aragua")
		pdf.ln(5)
		pdf.write(30,"5. Municipio: Girardot")
		pdf.ln(5)
		pdf.write(30,"6. Parroquia: Madre Maria")
		pdf.ln(5)
		pdf.write(30,"7. Dirección o Lugar: Complejo Cultural Santos Michelena Av Sucre c/c Princicpal de Calicanto".decode("UTF-8"))
		pdf.ln(5)
		pdf.write(30,"8. Fecha:")
		
		# Fila de la cabezera de la tabla
		pdf.ln(15)
		pdf.set_y(100)
		pdf.cell(24,5,"Clasificacion",'LTBR',1,'C',1)
		pdf.cell(8,5,"G",'LTBR',0,'C',1)
		pdf.cell(8,5,"S/G",'LTBR',0,'C',1)
		pdf.cell(8,5,"S",'LTBR',0,'C',1)
		
		pdf.set_y(100)
		pdf.set_x(34)
		pdf.cell(20,10,"Cantidad",'LTBR',0,'C',1)
		
		
		pdf.set_y(100)
		pdf.set_x(54)
		pdf.cell(25,10,"N Identificación".decode("UTF-8"),'LTBR',0,'C',1)
		
		pdf.set_y(100)
		pdf.set_x(79)
		pdf.cell(20,10,"Status",'LTBR',0,'C',1)
		
		pdf.set_y(100)
		pdf.set_x(99)
		pdf.cell(115,10,"Nombre Y Descripción del Elemento".decode("UTF-8"),'LTBR',0,'C',1)
		
		pdf.set_y(100)
		pdf.set_x(210)
		pdf.cell(30,10,"Valor Unitario Bs.",'LTBR',0,'C',1)
		
		pdf.set_y(100)
		pdf.set_x(240)
		pdf.cell(30,10,"Valor Total Bs.",'LTBR',1,'C',1)
		
		
		# Fin Cabezera
		pdf.set_font('Times','',10) # TAMANO DE LA FUENTE
		
		data_ids = self.read(cr, uid, ids, context=context)[0]
		payslip_id = data_ids['inventory_line_id'] # Grupo de IDS de la pre-nomina

		alm = self.pool.get('stock.inventory.line') # Objeto 
		datos = alm.search(cr, uid, [('id','=',payslip_id)], context=None)
		bienes = alm.read(cr,uid,datos,context=context)
		#print bienes
		j = 0
		suma = 0.0
		for i in bienes:
			if not float(i['v_unitario']):
				i['v_unitario'] = 0.0
			else:
				i['v_unitario']
			
			if not float(i['v_total']):
				i['v_total'] = 0.0
			else:
				i['v_total']
				
			if j == 12:
				pdf.add_page()	
				pdf.cell(0,-50,'Hoja N°: '.decode("UTF-8")+str(pdf.page_no()),0,0,'R') 	
				pdf.set_fill_color(255,255,255)
				pdf.set_font('Arial','B',12)
				pdf.cell(100,5,"",'',0,'C',1)
				pdf.cell(80,5,"Inventario de Bienes Muebles",'',0,'C',1)
				pdf.cell(75,5,"",'',0,'C',1)
				pdf.ln(0)
				pdf.set_font('Arial','B',8)
				pdf.write(30,"1. Entidad Propietaria: Gobierno del Estado Aragua")
				pdf.write(30,"2. Servicio:")
				pdf.ln(5)
				pdf.write(30,"3. Unidad de Trabajo o Dependencia:")
				pdf.ln(5)
				pdf.write(30,"4. Estado: Aragua")
				pdf.ln(5)
				pdf.write(30,"5. Municipio:")
				pdf.ln(5)
				pdf.write(30,"6. Parroquia:")
				pdf.ln(5)
				pdf.write(30,"7. Dirección o Lugar:".decode("UTF-8"))
				pdf.ln(5)
				pdf.write(30,"8. Fecha:")
				pdf.ln(20)
				
				# Fila de la cabezara de la tabla
				pdf.ln(20)
				pdf.set_y(100)
				pdf.cell(24,5,"Clasificacion",'LTBR',1,'C',1)
				pdf.cell(8,5,"G",'LTBR',0,'C',1)
				pdf.cell(8,5,"S/G",'LTBR',0,'C',1)
				pdf.cell(8,5,"S",'LTBR',0,'C',1)
		
				pdf.set_y(100)
				pdf.set_x(34)
				pdf.cell(20,10,"Cantidad",'LTBR',0,'C',1)
				pdf.set_y(100)
				pdf.set_x(54)
				pdf.cell(25,10,"N Identificación".decode("UTF-8"),'LTBR',0,'C',1)
		
				pdf.set_y(100)
				pdf.set_x(79)
				pdf.cell(20,10,"Status",'LTBR',0,'C',1)
		
				pdf.set_y(100)
				pdf.set_x(99)
				pdf.cell(115,10,"Nombre Y Descripción del Elemento".decode("UTF-8"),'LTBR',0,'C',1)
		
				pdf.set_y(100)
				pdf.set_x(210)
				pdf.cell(30,10,"Valor Unitario Bs.",'LTBR',0,'C',1)
		
				pdf.set_y(100)
				pdf.set_x(240)
				pdf.cell(30,10,"Valor Total Bs.",'LTBR',1,'C',1)
				
				# Fin Cabezera
				j=0
			
			# Filas que vienen de la BD
			pdf.set_font('Arial','',8)
			pdf.cell(8,5,str(i['g']),'LTBR',0,'C',1)
			pdf.cell(8,5,str(i['sg']),'LTBR',0,'C',1)
			pdf.cell(8,5,str(i['s']),'LTBR',0,'C',1)
			pdf.cell(20,5,str(i['product_qty']),'LTBR',0,'C',1)
			pdf.cell(25,5,str(i['nidentificacion']),'LTBR',0,'C',1)
			pdf.cell(20,5,str(i['estado']),'LTBR',0,'C',1)
			pdf.cell(111,5,str(i['product_id'][1]).decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(30,5,str(i['v_unitario']),'LTBR',0,'C',1)
			pdf.cell(30,5,str(i['v_total']),'LTBR',1,'C',1)
			suma = float(i['v_total']) + suma
			
			pdf.set_font('Times','',10) # TAMANO DE LA FUENTE
			j =j+1
			
			
		#pdf.ln(10)
		#pdf.write(30,"Total")
		pdf.set_font('Arial','B',8)
		pdf.cell(170,5,"",0,0,'C',0)
		pdf.cell(30,5,"Total en Bolivares",0,0,'C',0)
		pdf.cell(60,5,str(suma),'LTBR',1,'R',0)
		
		pdf.output('openerp/addons/producto_bva/reporte/ejemplo.pdf','F')
		
		archivo = open('openerp/addons/producto_bva/reporte/ejemplo.pdf')
		
		# Variables de tiempo (dia, mes, año) para que cada vez que 
		# se genere un reporte, al nombre se le adiera la fecha del día.
		dia = time.strftime('%d')
		mes = time.strftime('%m')
		year = time.strftime('%Y')
		fecha = dia+"-"+mes+"-"+year #Variable que concatena el dia la fecha y el año
		nom = 'Inventario '+fecha+'.pdf' #C
		
		r_archivo = self.pool.get('reporte.documentos').create(cr, uid, {
			'name' : nom,
			'res_name' : nom,
			'datas' : base64.encodestring(archivo.read()),
			'datas_fname' : nom,
			'res_model' : 'stock.inventory',
			},context=context)
		
		return r_archivo
	
	_columns = {
		'usuario_login': fields.many2one('res.users', 'Registrado por:', readonly=False),
		'ubicacion' : fields.many2one('stock.location', 'Área Solicitante', required=False),
	}

	_defaults = {
		'usuario_login': lambda s, cr, uid, c: uid,
	}
	
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
		values.update({
			'g' : obj_product.g,
			'sg' : obj_product.sg,
			's' : obj_product.s,
			'estado' : val,
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
 		'estado' : fields.char(string="Status", required=False),
 		'v_unitario' : fields.char(string="Valor Unitario Bs.", required=False),
 		'v_total' : fields.char(string="Valor Unitario Bs.", required=False),
 	}

