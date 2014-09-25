# -*- coding: utf-8 -*-
import class_pdf
import time
import base64
import random
import unicodedata
from time import gmtime, strftime
from openerp.osv import osv, fields
from datetime import datetime, timedelta
from openerp.tools.translate import _

class almacen_bva(osv.Model):

	_name = "inventario.almacen"
	

	def format_fecha(self, fecha):
		date = fecha.split("-")
		nueva_fecha = date[2]+"-"+date[1]+"-"+date[0]
		return nueva_fecha
	
	def generar_inventario_almacen(self, cr, uid, ids, context=None): # Generacion de inventario
		# Instancia de la clase heredada L es horizontal y P es vertical
		
		pdf=class_pdf.PDF3(orientation='P',unit='mm',format='letter' ) #HORIENTACION DE LA PAGINA
		
		#pdf.set_title(title)
		pdf.set_author('Marcel Arcuri')
		pdf.alias_nb_pages() # LLAMADA DE PAGINACION
		pdf.add_page() # AÑADE UNA NUEVA PAGINACION
		#pdf.set_font('Times','',10) # TAMANO DE LA FUENTE
		pdf.set_font('Arial','B',10)
		pdf.set_fill_color(157,188,201) # COLOR DE BOLDE DE LA CELDA
		pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
		#pdf.set_margins(8,10,10) # MARGENE DEL DOCUMENTO
		#pdf.ln(20) # Saldo de linea
		# 10 y 50 eje x y y 200 dimencion
		#pdf.line(10, 40, 200, 40) Linea
		
		
		prueba = self.browse(cr, uid, ids, context=context)
		pdf.ln(8)
		
		for x in prueba:
			nombre_r = x.nombre.encode("UTF-8").decode("UTF-8")
			fecha = self.format_fecha(x.date)
			realiza = x.usuario_login.name.encode("UTF-8").decode("UTF-8")
			pdf.set_fill_color(255,255,255)
			pdf.set_font('Arial','B',12)
			pdf.cell(55,5,"",'',0,'C',1)
			pdf.cell(80,5,"Inventario de la oficina al "+fecha,'',1,'C',1)
			pdf.cell(55,5,"",'',0,'C',1)
			pdf.cell(80,5,"Unidad de Bienes y Suministros",'',1,'C',1)
			pdf.cell(55,5,"",'',0,'C',1)
			pdf.cell(80,5,"A. C. Biblioteca Virtuales",'',1,'C',1)
			pdf.ln(15)


			# Fila de la cabezara de la tabla
			pdf.cell(13,5,"".decode("UTF-8"),'',0,'C',1)
			pdf.cell(15,5,"Ítem".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(25,5,"Cantidad".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(127,5,"Descripción del Material".decode("UTF-8"),'LTBR',1,'C',1)
		# Fin Cabezera
		
		
		data_ids = self.read(cr, uid, ids, context=context)[0]
		payslip_id = data_ids['almacen_m'] # Grupo de IDS

		alm = self.pool.get('inventario.materiales') # Objeto 
		datos = alm.search(cr, uid, [('id','=',payslip_id)], context=None)
		bienes = alm.read(cr,uid,datos,context=context)
		
		k = 0
		j = 0
		item = 0
		for i in bienes:
			if j == 25:
				
				pdf.add_page()
				pdf.ln(8)
				pdf.set_fill_color(255,255,255)
				pdf.set_font('Arial','B',12)
				pdf.cell(55,5,"",'',0,'C',1)
				pdf.cell(80,5,"Inventario de la oficina al "+fecha,'',1,'C',1)
				pdf.cell(55,5,"",'',0,'C',1)
				pdf.cell(80,5,"Unidad de Bienes y Suministros",'',1,'C',1)
				pdf.cell(55,5,"",'',0,'C',1)
				pdf.cell(80,5,"A. C. Biblioteca Virtuales",'',1,'C',1)
				pdf.ln(15)


				# Fila de la cabezara de la tabla
				pdf.cell(13,5,"".decode("UTF-8"),'',0,'C',1)
				pdf.cell(15,5,"Ítem".decode("UTF-8"),'LTBR',0,'C',1)
				pdf.cell(25,5,"Cantidad".decode("UTF-8"),'LTBR',0,'C',1)
				pdf.cell(127,5,"Descripción del Material".decode("UTF-8"),'LTBR',1,'C',1)


				# Fin Cabezera
				j=0
			
			# Filas que vienen de la BD
			item = int(item) + 1
			cant = int(i['cantidad'])
			unidad = str(i['unidad'][1]).encode("UTF-8").decode("UTF-8")
			if unidad == "11":
				unid = "Lt"
			else:
				unid = ""
			if unidad == "3":
				unid = "Kg"
			else:
				unid = ""

			
			pdf.set_font('Arial','',10)
			pdf.cell(13,5,"",'',0,'C',1)
			pdf.cell(15,5,str(item).decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(25,5,str(cant)+" "+unid,'LTBR',0,'C',1)
			pdf.cell(127,5,i['descripcion'][1].encode("UTF-8").decode("UTF-8"),'LTBR',1,'L',1)

			#if k == 24 : 
			#	pdf.ln(5)
			#	pdf.set_font('Arial','B',10)
			#	pdf.cell(13,5,"",'',0,'C',1)
			#	pdf.cell(84,6,"ENTREGADO",'LTBR',0,'C',0)
			#	pdf.cell(83,6,"SOLICITANTE",'LTBR',1,'C',1)
			#	
			#	pdf.cell(13,5,"",'',0,'C',1)
			#	pdf.cell(84,6,"Entregado por: "+reciv.decode("UTF-8"),'LTBR',0,'L',0)
			#	pdf.cell(83,6,"Recibido por: "+solic.decode("UTF-8"),'LTBR',1,'L',1)
			#	
			#	pdf.cell(13,5,"",'',0,'C',1)
			#	pdf.cell(84,6,"Fecha: "+fec_2,'LTBR',0,'L',0)
			#	pdf.cell(83,6,"Fecha: "+fec_2,'LTBR',1,'L',1)
			#	
			#	pdf.cell(13,5,"",'',0,'C',1)
			#	pdf.cell(84,6,"Firma:",'LTBR',0,'L',0)
			#	pdf.cell(83,6,"Firma:",'LTBR',1,'L',1)
			#
			## pdf.set_font('Arial','',8) # TAMANO DE LA FUENTE
			#	k = 0
			#
			#k = k+1
			j =j+1
			
		pdf.ln(5)
		pdf.set_font('Arial','B',10)
		pdf.cell(13,5,"",'',0,'C',1)
		pdf.cell(84,6,"REALIZADO POR",'LTBR',0,'C',0)
		pdf.cell(83,6,"SOLICITANTE",'LTBR',1,'C',1)
		
		pdf.cell(13,5,"",'',0,'C',1)
		pdf.cell(84,6,"Realizado por: "+realiza.decode("UTF-8"),'LTBR',0,'L',0)
		pdf.cell(83,6,"Recibido por: ",'LTBR',1,'L',1)
		
		pdf.cell(13,5,"",'',0,'C',1)
		pdf.cell(84,6,"Fecha: ",'LTBR',0,'L',0)
		pdf.cell(83,6,"Fecha: ",'LTBR',1,'L',1)
		
		pdf.cell(13,5,"",'',0,'C',1)
		pdf.cell(84,6,"Firma:",'LTBR',0,'L',0)
		pdf.cell(83,6,"Firma:",'LTBR',1,'L',1)
		
		nom = "Inventaro de Materiales y Suministros Totales al "+fecha+'.pdf' #Nombre del archivo .pdf

		
		pdf.output('openerp/addons/materiales_almacen/reportes/'+nom)
		#pdf.output('/home/administrador/openerp70/modules/producto_bva/reporte/'+nom,'F')
	
		archivo = open('openerp/addons/materiales_almacen/reportes/'+nom)
		#archivo = open('/home/administrador/openerp70/modules/producto_bva/reporte/'+nom)
		
		nom = "Inventaro de Materiales y Suministros Totales al "+fecha+'.pdf' #Nombre del archivo .pdf

		r_archivo = self.pool.get('reporte.inventario').create(cr, uid, {
		 	'name' : nom,
		 	'res_name' : nom,
		 	'datas' : base64.encodestring(archivo.read()),
		 	'datas_fname' : nom,
		 	'res_model' : 'inventario.almacen',
			'tipo_reporte': "Inventario Total"
		 	},context=context)
		
		return r_archivo

	_columns = {
		'nombre' : fields.char(string="Nombre de Referencia", required=True),
		'usuario_login': fields.many2one('res.users', 'Registrado por:', readonly=True),		
		'date': fields.date('Fecha de Creación', required=True, ),
		'almacen_m': fields.one2many('inventario.materiales', 'inventario_id', string='Materiales'),
	}
	_defaults = {
		#'date': lambda *a: time.strftime('%d/%m/%Y'),
		'usuario_login': lambda s, cr, uid, c: uid,
	}



class inventario_materiales(osv.Model):

	_name = "inventario.materiales"
	
	_columns = {
		'inventario_id':fields.many2one('inventario.almacen', 'inventario', ondelete='cascade', select=False),
		'cantidad' : fields.float(string="Cantidad", required=True),
		'gerencia' : fields.many2one('stock.location', 'Ubicación', required=False),
		'unidad':fields.many2one('product.uom', 'Unidad de Medida',required=True),
		't_materiales' : fields.selection((('1','Limpieza'), ('2','Oficina'), ('3','Servicios Generales'), ('4','Tecnológico')),'Tipo de Material', required=False),
		'descripcion':fields.many2one('materiales.almacen', 'Descripción del Material',required=False),
	}
	_defaults = {
		'gerencia': 23,
	}
	
	def on_change_inventario_materiales(self, cr, uid, ids, descripcion, gerencia, context=None):
		#print "GERENCIA: "+str(gerencia)
		#print "DESCRIPCION: "+str(descripcion)
		values = {}
		if not descripcion:
		    return {'value': {'cantidad': 0.0, 'unidad': False,}}
		datos = self.pool.get('materiales.almacen').browse(cr, uid, descripcion, context=context)
		uom = datos.unidad.id
		obj_product2 = self.pool.get('inventario.materiales')
		
		
		search_mate = obj_product2.search(cr,uid, [('gerencia','=', gerencia),('descripcion','=', descripcion)], context=None)
		read_mate        = obj_product2.read(cr, uid, search_mate, context=context)
		total = 0
		cant = 0.0
		for x in read_mate:
			if not x['cantidad']:
				cant = 0.0
			else:
				cant = x['cantidad']
			#total += cant

		values.update({
			'cantidad': cant,
			'unidad': uom,
		})
		return {'value': values}
	















