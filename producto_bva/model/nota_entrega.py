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

class nota_de_entrega(osv.Model):

	_name = "nota.entrega"
	
	_columns = {
		#'area' : fields.char(string="Área Solicitante:", required=True),
		'area' : fields.many2one('stock.location', 'Área Solicitante', required=True),
		'fecha': fields.char('Fecha:', readonly=True,  required=True),
		'nombre' : fields.char(string="Nota de Entrega:", required=True),
		'almacen': fields.one2many('materiales.bva', 'materiales_id', string='Materiales'),
		'solicitado' : fields.char(string="Solicitador por:", required=True),
		'recibido' : fields.char(string="Recibido por:", required=True),
		'c_nota' : fields.char(string="Correlativo:", size=6, readonly=True, required=True),
		'limpieza' : fields.boolean('Limpieza:'),
		'oficina' : fields.boolean('Oficina:'),
		'otros' : fields.boolean('Otros:'),
		#'t_materiales' : fields.selection((('Limpieza','Limpieza'), ('Oficina','Oficina'), ('Otros','Otros')),'Tipo de Material:', required=True),

	}
	def _get_last_id(self, cr, uid, ids, context = None):

                sfl_id       = self.pool.get('nota.entrega')
                srch_id      = sfl_id.search(cr,uid,[])
                rd_id        = sfl_id.read(cr, uid, srch_id, context=context)
                if rd_id:
                    id_documento = rd_id[-1]['c_nota']
                    c_nota = id_documento[2:]
                    last_id      = c_nota.lstrip('0')
                    str_number   = str(int(last_id) + 1)
                    last_id      = str_number.rjust(5,'0')
                    codigo      = last_id
                else :
                    str_number = '1'
                    last_id      = str_number.rjust(5,'0')
                    codigo      = last_id
                return codigo
	
	def procesar(self, cr, uid, ids, context=None): # Generacion de inventario
		
		obj_bva      = self.pool.get('materiales.bva') # Objeto 
		inventario  = self.pool.get('inventario.materiales') # Objeto 
		
		read_one = self.read(cr, uid, ids, context=context)[0]
		id_read_one = read_one['almacen'] # Grupo de IDS

		search_id  = obj_bva.search(cr, uid, [('id','=',id_read_one)], context=None) # Se busca el ID dado
		read_id  = obj_bva.read(cr,uid,search_id,context=context) # Se refleja el resultado
		

		for x in read_id:

			id_m_bva = x['descripcion'][0]
			cantidad_bva = x['cantidad']
			
			
			search_inv  = inventario.search(cr, uid, [('descripcion','=',id_m_bva)], context=None) # Se busca el ID dado
			materiales  = inventario.read(cr,uid,search_inv,context=context) # Se refleja el resultado
			
			for m in materiales:

				cantidad_materiales = m['cantidad']

				id_m_desc = m['descripcion'][0]

				
			resta_valor  =  int(cantidad_materiales) - int(cantidad_bva)


			
			if int(cantidad_bva) > int(cantidad_materiales):
				raise osv.except_osv(_("Warning!"), _("Disculpe no puede seleccionar una cantidad mayor a la que hay en existencia"))
			else:
				cr.execute("UPDATE inventario_materiales SET cantidad=%s WHERE descripcion=%s;", (resta_valor, id_m_desc))	

		return True


	def generar_nota_entrega(self, cr, uid, ids, context=None): # Generacion de inventario
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
			codigo = x.c_nota
			ubi = x.area.name.encode("UTF-8").decode("UTF-8")
			fecha = x.fecha
			solic = x.solicitado
			reciv = x.recibido
			nombre_n =x.nombre
			if x['limpieza'] == True:
				lim = 'X'
			else:
				lim = ''
			if x['oficina'] == True:
				ofi = 'X'
			else:
				ofi = ''
			if x['otros'] == True:
				otro = 'X'
			else:
				otro = ''
			
			
			
			pdf.set_fill_color(255,255,255)
			pdf.set_font('Arial','B',10)
			pdf.cell(160,6,"",'',0,'L',1)
			pdf.cell(20,6,"N° ".decode("UTF-8")+codigo,'LTBR',1,'L',1)
			pdf.ln(5)
			
			pdf.set_font('Arial','B',12)
			pdf.cell(55,5,"",'',0,'C',1)
			pdf.cell(80,5,"Nota de entrega",'',1,'C',1)
			pdf.ln(5)
			
			pdf.set_font('Arial','B',10)
			pdf.cell(13,6,"",'',0,'L',1)
			pdf.cell(107,6,"Área Solicitante: ".decode("UTF-8")+ubi,'LTBR',0,'L',1)
			pdf.cell(60,6,"Fecha: "+fecha ,'LTBR',1,'L',1)
			pdf.ln(5)
			
			pdf.set_font('Arial','B',10)
			pdf.cell(13,5,"".decode("UTF-8"),'',0,'C',1)
			pdf.cell(40,6,"Materiales",'LTBR',1,'C',1)
			pdf.cell(13,5,"".decode("UTF-8"),'',0,'C',1)
			pdf.cell(30,6,"Limpieza:",'LTB',0,'L',1)
			pdf.cell(10,6,lim,'LTBR',1,'C',1)
			pdf.cell(13,5,"".decode("UTF-8"),'',0,'C',1)
			pdf.cell(30,6,"Oficina:",'LTB',0,'L',1)
			pdf.cell(10,6,ofi,'LTBR',1,'C',1)
			pdf.cell(13,5,"".decode("UTF-8"),'',0,'C',1)
			pdf.cell(30,6,"Otros:",'LTB',0,'L',1)
			pdf.cell(10,6,otro,'LTBR',1,'C',1)
			pdf.ln(5)
			fec_2 = str(x['fecha'])
			# Fila de la cabezara de la tabla
			pdf.cell(13,5,"".decode("UTF-8"),'',0,'C',1)
			pdf.cell(15,5,"Ítem".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(25,5,"Cantidad".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(127,5,"Descripción del Material".decode("UTF-8"),'LTBR',1,'C',1)
		# Fin Cabezera
		pdf.set_font('Arial','',10) # TAMANO DE LA FUENTE
		
		data_ids = self.read(cr, uid, ids, context=context)[0]
		payslip_id = data_ids['almacen'] # Grupo de IDS

		alm = self.pool.get('materiales.bva') # Objeto 
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
				pdf.set_font('Arial','B',10)
				pdf.cell(160,6,"",'',0,'L',1)
				pdf.cell(20,6,"N° ".decode("UTF-8")+codigo,'LTBR',1,'L',1)
				pdf.ln(5)
				
				pdf.set_font('Arial','B',12)
				pdf.cell(55,5,"",'',0,'C',1)
				pdf.cell(80,5,"Nota de entrega",'',1,'C',1)
				pdf.ln(5)
				
				pdf.set_font('Arial','B',10)
				pdf.cell(13,6,"",'',0,'L',1)
				pdf.cell(107,6,"Área Solicitante: ".decode("UTF-8")+ubi,'LTBR',0,'L',1)
				pdf.cell(60,6,"Fecha: "+fecha ,'LTBR',1,'L',1)
				pdf.ln(5)
				
				pdf.set_font('Arial','B',10)
				pdf.cell(13,5,"".decode("UTF-8"),'',0,'C',1)
				pdf.cell(40,6,"Materiales",'LTBR',1,'C',1)
				pdf.cell(13,5,"".decode("UTF-8"),'',0,'C',1)
				pdf.cell(30,6,"Limpieza:",'LTB',0,'L',1)
				pdf.cell(10,6,lim,'LTBR',1,'C',1)
				pdf.cell(13,5,"".decode("UTF-8"),'',0,'C',1)
				pdf.cell(30,6,"Oficina:",'LTB',0,'L',1)
				pdf.cell(10,6,ofi,'LTBR',1,'C',1)
				pdf.cell(13,5,"".decode("UTF-8"),'',0,'C',1)
				pdf.cell(30,6,"Otros:",'LTB',0,'L',1)
				pdf.cell(10,6,otro,'LTBR',1,'C',1)

				pdf.ln(5)
				# Fin Cabezera
				j=0
			
			# Filas que vienen de la BD
			item = int(item) + 1
			unidad = str(i['unidad'][1]).encode("UTF-8").decode("UTF-8")
			if unidad == "Unidad(es)":
				unid = "Unidades"
			else:
				unid = ""
			if unidad == "Litro(s)":
				unid = "lts"
			else:
				unid = ""

			pdf.set_font('Arial','',10)
			pdf.cell(13,5,"",'',0,'C',1)
			pdf.cell(15,5,str(item).decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(25,5,str(i['cantidad'])+" "+unid,'LTBR',0,'C',1)
			pdf.cell(127,5,i['descripcion'][1].encode("UTF-8").decode("UTF-8"),'LTBR',1,'C',1)

			if k == 24 : 
				pdf.ln(5)
				pdf.set_font('Arial','B',10)
				pdf.cell(13,5,"",'',0,'C',1)
				pdf.cell(84,6,"ENTREGADO",'LTBR',0,'C',0)
				pdf.cell(83,6,"SOLICITANTE",'LTBR',1,'C',1)
				
				pdf.cell(13,5,"",'',0,'C',1)
				pdf.cell(84,6,"Entregado por: "+reciv.decode("UTF-8"),'LTBR',0,'L',0)
				pdf.cell(83,6,"Recibido por: "+solic.decode("UTF-8"),'LTBR',1,'L',1)
				
				pdf.cell(13,5,"",'',0,'C',1)
				pdf.cell(84,6,"Fecha: "+fec_2,'LTBR',0,'L',0)
				pdf.cell(83,6,"Fecha: "+fec_2,'LTBR',1,'L',1)
				
				pdf.cell(13,5,"",'',0,'C',1)
				pdf.cell(84,6,"Firma:",'LTBR',0,'L',0)
				pdf.cell(83,6,"Firma:",'LTBR',1,'L',1)
			
			# pdf.set_font('Arial','',8) # TAMANO DE LA FUENTE
				k = 0

			k = k+1
			j =j+1
			
		pdf.ln(5)
		pdf.set_font('Arial','B',10)
		pdf.cell(13,5,"",'',0,'C',1)
		pdf.cell(84,6,"ENTREGADO",'LTBR',0,'C',0)
		pdf.cell(83,6,"SOLICITANTE",'LTBR',1,'C',1)
		
		pdf.cell(13,5,"",'',0,'C',1)
		pdf.cell(84,6,"Entregado por: "+reciv.decode("UTF-8"),'LTBR',0,'L',0)
		pdf.cell(83,6,"Recibido por: "+solic.decode("UTF-8"),'LTBR',1,'L',1)
		
		pdf.cell(13,5,"",'',0,'C',1)
		pdf.cell(84,6,"Fecha: "+fec_2,'LTBR',0,'L',0)
		pdf.cell(83,6,"Fecha: "+fec_2,'LTBR',1,'L',1)
		
		pdf.cell(13,5,"",'',0,'C',1)
		pdf.cell(84,6,"Firma:",'LTBR',0,'L',0)
		pdf.cell(83,6,"Firma:",'LTBR',1,'L',1)
		
		nom = nombre_n+'.pdf'
		pdf.output('/home/administrador/openerp70/modules/producto_bva/reporte/'+nom,'F')
	
		#archivo = open('openerp/addons/planificacion_presupuesto/reportes/'+nom)
		archivo = open('/home/administrador/openerp70/modules/producto_bva/reporte/'+nom)
		
		nom = nombre_n+" "+fecha+'.pdf' #Nombre del archivo .pdf

		r_archivo = self.pool.get('reporte.documentos').create(cr, uid, {
				'name' : nom,
				'res_name' : nom,
				'datas' : base64.encodestring(archivo.read()),
				'datas_fname' : nom,
				'res_model' : 'nota.entrega',
				'tipo_reporte': "Nota de Entrega"
			},context=context)
		
		return r_archivo
		
	_defaults = {
		'fecha': lambda *a: time.strftime("%d-%m-%Y"),
		'c_nota' : _get_last_id
	} 

class materiales_bva(osv.Model):

	_name = "materiales.bva"
	
	_columns = {
		'materiales_id':fields.many2one('nota.entrega', 'almacen', ondelete='cascade', select=False),
		'cantidad' : fields.integer(string="Cantidad Solicitada", required=True),
		'cantidad_stock' : fields.float(string="Cantidad en existencia", required=False),
		'unidad':fields.many2one('product.uom', 'Unidad de Medida',required=True),
		'descripcion':fields.many2one('materiales.almacen', 'Descripción del Material',required=True),
	}
	

	def on_change_cantidades(self, cr, uid, ids, descripcion, context=None):
		
		values = {}
		if not descripcion:
			return values
		
		unid = self.pool.get('materiales.almacen').browse(cr, uid, descripcion, context=context)
		uom = unid.unidad.id
		
		datos = self.pool.get('inventario.materiales')
		variable = datos.search(cr, uid, [('descripcion','=',descripcion)], context=None)
		rd_id  = datos.read(cr, uid, variable, context=None)
		
		if not variable:
			raise osv.except_osv(_("Warning!"), _("Disculpe el material aun no ha sido inventariado"))
		
			return False	
		else:
			existencia = rd_id[0]['cantidad']
			
		values.update({
			'cantidad_stock' : existencia,
			'unidad': uom,
		})
		return {'value' : values}
	
	def on_change_comparar(self, cr, uid, ids, cantidad, cantidad_stock, context=None):
		
		
		if int(cantidad) > int(cantidad_stock):
			raise osv.except_osv(_("Warning!"), _("Disculpe no puede seleccionar una cantidad mayor a la que hay en existencia"))
		return True
