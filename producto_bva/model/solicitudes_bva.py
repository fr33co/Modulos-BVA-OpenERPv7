# -*- coding: utf-8 -*-

import class_pdf
import time
import base64
import random
import unicodedata
from time import gmtime, strftime
from openerp.osv import osv, fields
from datetime import datetime, timedelta

class solicitudes_bva(osv.Model):

	_name = "solicitudes.bva"
	
	# Acciones de cada uno de los botones de la barra de estado de solicitud
	#def action_exportar(self, cr, uid, ids, context = None):
	#return self.write(cr, uid, ids, {'generar':'Generar Solicitud'}, context=context)

	# def action_confirmar(self, cr, uid, ids, context = None):
	# 	return self.write(cr, uid, ids, {'generar':'Confirmado'}, context=context)

	# def action_borrador(self, cr, uid, ids, context = None):
	# 	return self.write(cr, uid, ids, {'generar':'Borrador'}, context=context)
        
        """
	Metodo que genera el codigo 
	"""

	def _get_id_solicitudes(self, cr, uid, ids, context = None):
	
		sfl_id       = self.pool.get('solicitudes.bva')
		srch_id      = sfl_id.search(cr,uid,[])
		rd_id        = sfl_id.read(cr, uid, srch_id, context=context)
		

		if rd_id:
			id_documento = rd_id[-1]['correlativo']
			codigo = id_documento[3:]
			last_id      = codigo.lstrip('0')
			str_number   = str(int(last_id) + 1)
			codigo      = str_number.rjust(4,'0')
			print codigo
		else :
			str_number = '1'
			last_id      = str_number.rjust(4,'0')
			codigo      = last_id
		return codigo

	# def elimina_tildes(self, s):
    	
 #    	return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

	def generar_solicitud(self, cr, uid, ids, context=None): # Generacion de inventario
		# Instancia de la clase heredada L es horizontal y P es vertical
		
		pdf=class_pdf.PDF2(orientation='L',unit='mm',format='letter' ) #HORIENTACION DE LA PAGINA
		
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
		pdf.ln(5)
		for x in prueba:
			pdf.set_fill_color(255,255,255)
			pdf.set_font('Arial','B',10)
			pdf.cell(35,5,"Area Solicitante:", 'LTB',0,'L',1)
			pdf.cell(115,5,x.area.name.encode("UTF-8").decode("UTF-8"), 'TBR',0,'L',1)
			pdf.cell(15,5,"Fecha:",'LTB',0,'L',1)
			pdf.cell(40,5, str(x['fecha']), 'TBR',0,'L',1)
			pdf.cell(25,5,"Correlativo:",'LTB',0,'L',1)
			pdf.cell(30,5,str(x['correlativo']),'TBR',1,'L',1)		
			pdf.ln(4)

			area = x.area.name.encode("UTF-8").decode("UTF-8")
			fecha = str(x['fecha'])
			corre = str(x['correlativo'])
			nombre_s = x.nombre.encode("UTF-8").decode("UTF-8")
			
			pdf.set_font('Arial','B',12)
			pdf.cell(100,5,"",'',0,'C',1)
			pdf.cell(80,5,"SOLICITUD DE MATERIALES, SUMINISTROS Y EQUIPOS",'',1,'C',1)
			pdf.ln(4)
			
			pdf.set_font('Arial','B',10)
			pdf.cell(115,6,"",'LTB',0,'C',1)
			pdf.cell(105,6,"MATERIAL:",'TB',0,'L',1)
			pdf.cell(40,6,"",'TBR',1,'C',1)
			if x['limpieza'] == True:
				lim = 'X'
			else:
				lim = ''
			if x['s_generales'] == True:
				ser = 'X'
			else:
				ser = ''
			if x['oficina_papeleria'] == True:
				ofi = 'X'
			else:
				ofi = ''
			if x['tecnologico'] == True:
				tec = 'X'
			else:
				tec = ''
			if x['otros'] == True:
				otro = 'X'
			else:
				otro = ''
			pdf.set_font('Arial','B',10)
			pdf.cell(30,5,"Limpieza:",'LTB',0,'R',1)
			pdf.cell(10,5,lim,'TBR',0,'L',1)
			pdf.cell(55,5,"Servicios Generales:",'LTB',0,'R',1)
			pdf.cell(10,5,ser,'TBR',0,'L',1)
			pdf.cell(55,5,"Oficina o papeleria:",'LTB',0,'R',1)
			pdf.cell(10,5,ofi,'TBR',0,'L',1)
			pdf.cell(40,5,"Tecnológico:".decode("UTF-8"),'LTB',0,'R',1)
			pdf.cell(10,5,tec,'TBR',0,'L',1)
			pdf.cell(30,5,"Otros:",'LTB',0,'R',1)
			pdf.cell(10,5,otro,'TBR',1,'L',1)
			pdf.ln(3)
			
			pdf.set_font('Arial','B',10)
			pdf.cell(200,4,"",'',0,'C',1)
			pdf.cell(60,4,"Espacio para ser".decode("UTF-8"),'LTR',1,'C',1)
			pdf.set_font('Arial','B',10)
			pdf.cell(200,4,"",'',0,'C',1)
			pdf.cell(60,4,"llenado por Almacén:".decode("UTF-8"),'LBR',1,'C',1)
			
			# Fila de la cabezara de la tabla
			
			pdf.cell(15,8,"Ítem".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(50,8,"Material requerido",'LTBR',0,'C',1)
			pdf.cell(20,8,"Cantidad".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,8,"Modelo",'LTBR',0,'C',1)
			pdf.cell(25,8,"Marca".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(40,8,"Inform. Adicional",'LTBR',0,'C',1)
			pdf.cell(30,8,"Foto ",'LTBR',0,'C',1)
			pdf.cell(30,8,"En Existencia",'LTBR',0,'C',1)
			pdf.cell(30,8,"Requerimiento",'LTBR',1,'C',1)
			log = x.solicitado.name.encode("UTF-8").decode("UTF-8")
			fec_2 = str(x['fecha_rep'])
		# Fin Cabezera
		pdf.set_font('Arial','',10) # TAMANO DE LA FUENTE
		
		data_ids = self.read(cr, uid, ids, context=context)[0]
		payslip_id = data_ids['almacen'] # Grupo de IDS

		alm = self.pool.get('solicitud.materiales') # Objeto 
		datos = alm.search(cr, uid, [('id','=',payslip_id)], context=None)
		bienes = alm.read(cr,uid,datos,context=context)
		
		k = 0
		j = 0
		item = 0
		for i in bienes:
			if j == 20:
				
				pdf.add_page()
				pdf.ln(5)		
				pdf.set_font('Arial','B',10)
				pdf.cell(35,5,"Area Solicitante:", 'LTB',0,'L',1)
				pdf.cell(115,5, area, 'TBR',0,'L',1)
				pdf.cell(15,5,"Fecha:",'LTB',0,'L',1)
				pdf.cell(40,5, fecha, 'TBR',0,'L',1)
				pdf.cell(25,5,"Correlativo:",'LTB',0,'L',1)
				pdf.cell(30,5, corre,'TBR',1,'L',1)		
				pdf.ln(4)
		
				pdf.set_font('Arial','B',12)
				pdf.cell(100,5,"",'',0,'C',1)
				pdf.cell(80,5,"SOLICITUD DE MATERIALES, SUMINISTROS Y EQUIPOS",'',1,'C',1)
				pdf.ln(4)
		
				pdf.set_font('Arial','B',10)
				pdf.cell(105,5,"",'LTB',0,'C',1)
				pdf.cell(105,5,"MATERIAL:",'TB',0,'L',1)
				pdf.cell(50,5,"",'TBR',1,'C',1)
		
				pdf.set_font('Arial','B',10)
				pdf.cell(30,5,"Limpieza:",'LTB',0,'R',1)
				pdf.cell(10,5,lim,'TBR',0,'L',1)
				pdf.cell(55,5,"Servicios Generales:",'LTB',0,'R',1)
				pdf.cell(10,5,ser,'TBR',0,'L',1)
				pdf.cell(55,5,"Oficina o papeleria:",'LTB',0,'R',1)
				pdf.cell(10,5,ofi,'TBR',0,'L',1)
				pdf.cell(40,5,"Tecnológico:".decode("UTF-8"),'LTB',0,'R',1)
				pdf.cell(10,5,tec,'TBR',0,'L',1)
				pdf.cell(30,5,"Otros:",'LTB',0,'R',1)
				pdf.cell(10,5,otro,'TBR',1,'L',1)
				pdf.ln(3)
		
				pdf.set_font('Arial','B',10)
				pdf.cell(215,5,"",'',0,'C',1)
				pdf.cell(45,5,"Espacio para ser".decode("UTF-8"),'LTR',1,'C',1)
				pdf.set_font('Arial','B',10)
				pdf.cell(215,5,"",'',0,'C',1)
				pdf.cell(45,5,"llenado por Almacén:".decode("UTF-8"),'LBR',1,'C',1)
				
				# Fila de la cabezara de la tabla
			
				pdf.cell(15,8,"Ítem".decode("UTF-8"),'LTBR',0,'C',1)
				pdf.cell(50,8,"Material requerido",'LTBR',0,'C',1)
				pdf.cell(20,8,"Cantidad".decode("UTF-8"),'LTBR',0,'C',1)
				pdf.cell(20,8,"Modelo",'LTBR',0,'C',1)
				pdf.cell(25,8,"Marca".decode("UTF-8"),'LTBR',0,'C',1)
				pdf.cell(40,8,"Inform. Adicional",'LTBR',0,'C',1)
				pdf.cell(30,8,"Foto ",'LTBR',0,'C',1)
				pdf.cell(30,8,"En Existencia",'LTBR',0,'C',1)
				pdf.cell(30,8,"Requerimiento",'LTBR',1,'C',1)
				# Fin Cabezera
				j=0
			
			# Filas que vienen de la BD
			item = int(item) + 1
			pdf.set_font('Arial','',8)
			pdf.cell(15,5,str(item),'LTBR',0,'C',1)
			pdf.cell(50,5,i['descripcion'][1].encode("UTF-8").decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(20,5,str(i['cantidad']),'LTBR',0,'C',1)
			pdf.cell(20,5,"",'LTBR',0,'C',1)
			pdf.cell(25,5,"",'LTBR',0,'C',1)
			pdf.cell(40,5,".",'LTBR',0,'C',1)
			pdf.cell(30,5," ",'LTBR',0,'C',1)
			pdf.cell(30,5," ",'LTBR',0,'C',1)
			pdf.cell(30,5,"",'LTBR',1,'C',1)

			if k == 19 : 
				pdf.ln(5)
				pdf.set_font('Arial','B',10)
				pdf.cell(70,5,"Solicitado por:",'LTBR',0,'C',0)
				pdf.cell(70,5,"Recibido por:",'LTBR',0,'C',0)
				pdf.cell(70,5,"Revisador por Compras:",'LTBR',1,'C',0)
				
				pdf.cell(70,5,log,'LTBR',0,'C',0)
				pdf.cell(70,5,"",'LTBR',0,'C',0)
				pdf.cell(70,5,"",'LTBR',1,'C',0)
				
				pdf.cell(15,5,"Fecha:",'LTB',0,'L',0)
				pdf.cell(55,5,fec_2,'TBR',0,'L',0)
				pdf.cell(70,5,"Fecha:",'LTBR',0,'L',0)
				pdf.cell(70,5,"Fecha:",'LTBR',1,'L',0)
				
				pdf.cell(70,5,"Firma:",'LTBR',0,'L',0)
				pdf.cell(70,5,"Firma:",'LTBR',0,'L',0)
				pdf.cell(70,5,"Firma:",'LTBR',1,'L',0)
			
			# pdf.set_font('Arial','',8) # TAMANO DE LA FUENTE
				k = 0

			k = k+1
			j =j+1
			
		pdf.ln(5)
		pdf.set_font('Arial','B',10)
		pdf.cell(70,5,"Solicitado por:",'LTBR',0,'C',0)
		pdf.cell(70,5,"Recibido por:",'LTBR',0,'C',0)
		pdf.cell(70,5,"Revisador por Compras:",'LTBR',1,'C',0)
		
		pdf.cell(70,5,log,'LTBR',0,'C',0)
		pdf.cell(70,5,"",'LTBR',0,'C',0)
		pdf.cell(70,5,"",'LTBR',1,'C',0)
		
		pdf.cell(15,5,"Fecha:",'LTB',0,'L',0)
		pdf.cell(55,5,fec_2,'TBR',0,'L',0)
		pdf.cell(70,5,"Fecha:",'LTBR',0,'L',0)
		pdf.cell(70,5,"Fecha:",'LTBR',1,'L',0)
		
		pdf.cell(70,5,"Firma:",'LTBR',0,'L',0)
		pdf.cell(70,5,"Firma:",'LTBR',0,'L',0)
		pdf.cell(70,5,"Firma:",'LTBR',1,'L',0)
		
		pdf.output('openerp/addons/producto_bva/reporte/ejemplo2.pdf','F')
		
		archivo = open('openerp/addons/producto_bva/reporte/ejemplo2.pdf')
		
		nom = nombre_s+" "+fecha+'.pdf' #Nombre del archivo .pdf

		r_archivo = self.pool.get('reporte.documentos').create(cr, uid, {
		 	'name' : nom,
		 	'res_name' : nom,
		 	'datas' : base64.encodestring(archivo.read()),
		 	'datas_fname' : nom,
		 	'res_model' : 'nota.entrega',
			'tipo_reporte': "Solicitudes de Almacen"
		 	},context=context)
		
		return r_archivo
		

		
	_columns = {
		'area' : fields.many2one('stock.location', 'Área Solicitante', required=True),
		'fecha': fields.char('Fecha:', readonly=True,  required=True),
		'fecha_rep': fields.char('Fecha2:'),
		'correlativo' : fields.char(string="Correlativo", readonly=True, required=False),
		'limpieza' : fields.boolean('Limpieza:'),
		's_generales' : fields.boolean('Servicios Generales:'),
		'oficina_papeleria' : fields.boolean('Oficina Papeleria:'),
		'tecnologico' : fields.boolean('Técnologico:'),
		'otros' : fields.boolean('Otros:'),
		'nombre' : fields.char(string="Nombre de referencia:", required=True),
		'almacen': fields.one2many('solicitud.materiales', 'materiales_id', string='Materiales'),
		'solicitado' : fields.many2one('res.users', 'Solicitado por:', readonly=True),

	}

        _defaults = {
		'fecha': lambda *a: time.strftime("%d/%m/%Y"),
		'fecha_rep': lambda *a: time.strftime("%d de %B %Y"),
		'correlativo' : _get_id_solicitudes,
		'solicitado': lambda s, cr, uid, c: uid,

	}
	
class solicitud_materiales(osv.Model):

	_name = "solicitud.materiales"
	
	_columns = {
		'materiales_id':fields.many2one('solicitudes.bva', 'almacen', ondelete='cascade', select=False),
		'cantidad' : fields.char(string="Cantidad", required=True),
		#'item' : fields.char(string="Item", required=False),
		#'unidad':fields.many2one('product.uom', 'Unidad de Medida',required=True),
		'descripcion':fields.many2one('materiales.almacen', 'Descripción del Material',required=True),
	}