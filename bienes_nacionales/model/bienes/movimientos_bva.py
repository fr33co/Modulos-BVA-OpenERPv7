# -*- coding: utf-8 -*-
import class_pdf
import time
import base64
import random
import unicodedata
from time import gmtime, strftime
from openerp.osv import osv, fields
from datetime import datetime, timedelta

class movimientos_gba(osv.Model):

	_inherit = "stock.move"

	"""
	Metodo que genera el codigo 
	"""

	#def _get_id_movimientos(self, cr, uid, ids, context = None):
	#
	#	sfl_id       = self.pool.get('stock.move')
	#	srch_id      = sfl_id.search(cr,uid,[])
	#	rd_id        = sfl_id.read(cr, uid, srch_id, context=context)
	#	
	#
	#	if rd_id:
	#		id_documento = rd_id[-1]['correlativo']
	#		codigo = id_documento[3:]
	#		last_id      = codigo.lstrip('0')
	#		str_number   = str(int(last_id) + 1)
	#		codigo      = str_number.rjust(4,'0')
	#		print codigo
	#	else :
	#		str_number = '1'
	#		last_id      = str_number.rjust(4,'0')
	#		codigo      = last_id
	#	return codigo
	
	#MÉTODO PARA GENERAR EL NÚMERO CORRELATIVO POR DEFECTO
	def _gen_correlativo(self, cr, uid, ids, context=None):
			
		correlativo_mov = ""        
			
		cr.execute("SELECT count(*) as num_movimientos FROM stock_move")
		num_movimientos = cr.fetchone()[0]
			
		anyo = time.strftime("%Y")
			
		correlativo_mov = str(num_movimientos+1).zfill(6)+"-"+anyo
				
				
		return correlativo_mov
	
	def onchange_product_id(self, cr, uid, ids, prod_id=False, loc_id=False, loc_dest_id=False, partner_id=False):
		""" On change of product id, if finds UoM, UoS, quantity and UoS quantity.
		@param prod_id: Changed Product id
		@param loc_id: Source location id
		@param loc_dest_id: Destination location id
		@param partner_id: Address id of partner
		@return: Dictionary of values
		"""
		if not prod_id:
		    return {}
		user = self.pool.get('res.users').browse(cr, uid, uid)
		lang = user and user.lang or False
		if partner_id:
		    addr_rec = self.pool.get('res.partner').browse(cr, uid, partner_id)
		    if addr_rec:
			lang = addr_rec and addr_rec.lang or False
		ctx = {'lang': lang}
	
		product = self.pool.get('product.product').browse(cr, uid, [prod_id], context=ctx)[0]
		uos_id  = product.uos_id and product.uos_id.id or False
		result = {
			'product_uom': product.uom_id.id,
			'product_uos': uos_id,
			'product_qty': 1.00,
			'product_uos_qty' : self.pool.get('stock.move').onchange_quantity(cr, uid, ids, prod_id, 1.00, product.uom_id.id, uos_id)['value']['product_uos_qty'],
			'prodlot_id' : False,
			's': product.s,
			'g' : product.g,
			'sg' : product.sg,
			'estado' : product.estado,
			'bva' : product.nidentificacion,
			#'cantidad' : datos.cantidad,
			'v_total' : product.v_total,
		}
		if not ids:
		    result['name'] = product.partner_ref
		if loc_id:
		    result['location_id'] = loc_id
		if loc_dest_id:
		    result['location_dest_id'] = loc_dest_id
		return {'value': result}
	
	def format_fecha(self, fecha):
		date = fecha.split("-")
		nueva_fecha = date[2]+"-"+date[1]+"-"+date[0]
		return nueva_fecha
	
	def generar_movimiento(self, cr, uid, ids, context=None): # Generacion de inventario
		# Instancia de la clase heredada L es horizontal y P es vertical
		
		pdf=class_pdf.PDF5(orientation='P',unit='mm',format='letter' ) #HORIENTACION DE LA PAGINA
		
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
		
		
		move = self.browse(cr, uid, ids, context=context)
		pdf.ln(5)
		for x in move:
			t_mov = str(x['tipo_envio'])
			dia= self.format_fecha(x.fecha)
			codigo = str(x['correlativo'])+"-"+str(x['f_correlativo'])
			just = x.justificacion.encode("UTF-8").decode("UTF-8")
			#nota = x.nota.encode("UTF-8").decode("UTF-8")
			descripcion = acento(x.name)
			origen = acento(x.location_id.name)
			destino = acento(x.location_dest_id.name)
			env = acento(x.enviado)
			rec = acento(x.recibido)
			vig = acento(x.vigilante)
			cantidad = int(x['product_qty'])
			v_total = float(x['v_total'])
			total = addComa(str(v_total))
			id_pro = x.product_id.id
			ubic_f = x.location_dest_id.id
			fecha = x.fecha
			if x.estado == '1':
				esta = 'Bueno'
			else:
				esta = 'Malo'
				
			pdf.ln(5)
			pdf.set_fill_color(255,255,255)
			pdf.set_font('Arial','B',12)
			pdf.cell(55,6,"",'',0,'L',1)
			pdf.cell(100,6,"CONTROL DE TRASLADO DE BIENES MUEBLES".decode("UTF-8"),'',1,'L',1)
			pdf.ln(5)
			
			pdf.set_font('Arial','B',10)
			pdf.cell(5,5,"",'',0,'C',1)
			pdf.cell(92,5,"Tipo de Movimiento: ",'LTBR',0,'L',1)
			pdf.cell(93,5,"Fecha: "+dia ,'LTBR',1,'L',1)
			pdf.cell(5,5,"",'',0,'L',1)
			pdf.cell(92,5,t_mov,'LTBR',0,'L',1)
			pdf.cell(93,5,"Correlativo: "+codigo,'LTBR',1,'L',1)
			pdf.ln(5)
			
			pdf.set_font('Arial','B',10)
			pdf.cell(5,5,"",'',0,'L',1)
			pdf.cell(92,5,"Lugar de Origen: "+origen,'LTBR',0,'L',1)
			pdf.cell(93,5,"Nombre Responsable: "+env,'LTBR',1,'L',1)
			pdf.cell(5,5,"",'',0,'L',1)
			pdf.cell(92,5,"Lugar de Destino: "+destino,'LTBR',0,'L',1)
			pdf.cell(93,5,"Nombre Responsable: "+rec,'LTBR',1,'L',1)
			
			
			pdf.set_font('Arial','B',10)
			pdf.cell(5,5,"",'',0,'L',1)
			pdf.set_fill_color(191,191,191)
			pdf.cell(185,5,"Justificación".decode("UTF-8"),'LTBR',1,'C',1)
			
			pdf.set_fill_color(255,255,255)
			pdf.set_font('Arial','',10)
			pdf.cell(5,5,"",'',0,'L',1)
			pdf.cell(185,5,just,'LTBR',1,'C',1)
			
			
			pdf.set_y(81)
			pdf.cell(5,5,"",'',0,'L',1)
			pdf.set_fill_color(191,191,191)
			pdf.set_font('Arial','B',8)
			pdf.cell(24,5,"Clasificacion",'LTBR',1,'C',1)
			pdf.set_fill_color(255,255,255)
			pdf.cell(5,5,"",'',0,'L',1)
			pdf.set_fill_color(191,191,191)
			pdf.cell(8,5,"G",'LTBR',0,'C',1)
			pdf.cell(8,5,"S/G",'LTBR',0,'C',1)
			pdf.cell(8,5,"S",'LTBR',0,'C',1)
			
			pdf.set_y(81)
			pdf.set_x(39)
			pdf.cell(15,10,"Cantidad",'LTBR',0,'C',1)
			
			pdf.set_y(81)
			pdf.set_x(54)
			pdf.cell(23,10,"N Identificación".decode("UTF-8"),'LTBR',0,'C',1)
			
			pdf.set_y(81)
			pdf.set_x(77)
			pdf.cell(13,10,"Estatus",'LTBR',0,'C',1)
			
			pdf.set_y(81)
			pdf.set_x(90)
			pdf.cell(95,10,"Nombre Y Descripción del Elemento".decode("UTF-8"),'LTBR',0,'C',1)
			
			pdf.set_y(81)
			pdf.set_x(185)
			pdf.cell(15,10,"Valor Bs.",'LTBR',1,'C',1)
			
			pdf.set_font('Arial','',8)
			pdf.set_fill_color(255,255,255)
			pdf.cell(5,5,"",'',0,'L',1)
			pdf.cell(8,6,x.s,'LTBR',0,'C',1)
			pdf.cell(8,6,x.sg,'LTBR',0,'C',1)
			pdf.cell(8,6,x.g,'LTBR',0,'C',1)
			pdf.cell(15,6,str(cantidad),'LTBR',0,'C',1)
			pdf.cell(23,6,x.bva,'LTBR',0,'C',1)
			pdf.cell(13,6,esta,'LTBR',0,'C',1)
			pdf.set_font('Arial','',7)
			pdf.cell(95,6,descripcion,'LTBR',0,'C',1)
			pdf.set_font('Arial','',8)
			pdf.cell(15,6,str(v_total),'LTBR',1,'C',1)
			
			
			pdf.set_font('Arial','B',8)
			pdf.cell(5,5,"",'',0,'L',1)
			pdf.set_fill_color(191,191,191)
			pdf.cell(39,6,"Entregado por",'LTBR',0,'C',1)
			pdf.cell(36,6,"Recibido por ",'LTBR',0,'C',1)
			pdf.cell(46,6,"Vigilante de Guardia",'LTBR',0,'C',1)
			pdf.cell(64,6,"Unidad de Bienes",'LTBR',1,'C',1)
			
			pdf.set_fill_color(255,255,255)
			pdf.set_font('Arial','',8)
			pdf.cell(5,5,"",'',0,'L',1)
			pdf.cell(39,6,env,'LTR',0,'C',1)
			pdf.cell(36,6,rec,'LTR',0,'C',1)
			pdf.cell(46,6,vig,'LTR',0,'C',1)
			pdf.cell(64,6,"Ana Mendivelso",'LTR',1,'C',1)
			pdf.cell(5,5,"",'',0,'L',1)
			pdf.cell(39,6,"",'LBR',0,'C',1)
			pdf.cell(36,6,"",'LBR',0,'C',1)
			pdf.cell(46,6,"",'LBR',0,'C',1)
			pdf.cell(64,6,"Jefe de la unidad de Bienes y Suministros (E)",'LBR',1,'C',1)
			
			pdf.set_font('Arial','B',10)
			pdf.cell(5,5,"",'',0,'L',1)
			pdf.set_fill_color(191,191,191)
			pdf.cell(185,5,"Nota".decode("UTF-8"),'LTBR',1,'C',1)
			
			pdf.set_font('Arial','',9)
			pdf.set_fill_color(255,255,255)
			pdf.cell(5,5,"",'',0,'L',1)
			pdf.cell(185,5,"SE HACE RESPONSABLE QUIEN RECIBA LOS BIENES, DAR BUEN USO Y MANEJO DE LOS MISMOS.  IGUALMENTE".decode("UTF-8"),'LTR',1,'C',1)
			pdf.cell(5,5,"",'',0,'L',1)
			pdf.cell(185,5,"QUIEN ENTREGA, DEBE NOTIFICAR A LA UNIDAD DE BIENES, EN UN PLAZO NO MAYOR A TRES DÍAS HÁBILES,".decode("UTF-8"),'LR',1,'C',1)
			pdf.cell(5,5,"",'',0,'L',1)
			pdf.cell(185,5,"ENVIANDO PARA TAL EFECTO COPIA DE ESTE FORMATO.".decode("UTF-8"),'LBR',1,'C',1)
			
			cr.execute("UPDATE product_product SET ubicacion=%s WHERE id=%s;", (ubic_f, id_pro))
		
		nom = codigo+'.pdf' #Nombre del archivo .pdf

		pdf.output('openerp/addons/bienes_nacionales/reportes/'+nom,'F')

		#archivo = open('/home/administrador/openerp70/modules/producto_bva/reporte/'+nom)
		archivo = open('openerp/addons/bienes_nacionales/reportes/'+nom)
		#pdf.output('/home/administrador/openerp70/modules/producto_bva/reporte/'+nom,'F')
	
		#archivo = open('openerp/addons/planificacion_presupuesto/reportes/'+nom)
		#archivo = open('/home/administrador/openerp70/modules/producto_bva/reporte/'+nom)
		
		#nom = "Movimiento de "+descripcion+" "+fecha+'.pdf' #Nombre del archivo .pdf
		#
		#r_archivo = self.pool.get('reporte.documentos').create(cr, uid, {
		# 	'name' : nom,
		# 	'res_name' : nom,
		# 	'datas' : base64.encodestring(archivo.read()),
		# 	'datas_fname' : nom,
		# 	'res_model' : 'stock.move',
		#	'tipo_reporte': "Movimiento de Bien",
		#	},context=context)
		#
		#return r_archivo
		return True 
		
	_columns = {
		'enviado' : fields.char(string="Responsable", size=50, required=False),
		'recibido' : fields.char(string="Responsable", size=50, required=False),
		'vigilante' : fields.char(string="Vigilante de Guardia", size=50, required=False),
		'g' : fields.char(string="G", required=False),
		'sg' : fields.char(string="S/G", required=False),
		's' : fields.char(string="S", required=False),
		'bva' : fields.char(string="N de Identificacion"),
		'estado' : fields.selection((('1','Bueno'), ('2','Malo')),'Status', required=True),
		'v_total' : fields.float(string="Valor Unitario Bs.", required=False),
		'nota' : fields.text(string="Nota", required=False),
		'correlativo' : fields.char(string="Correlativo", readonly=True, required=False),
		'justificacion' : fields.char(string="Justificación", required=False),
		'f_correlativo': fields.char('Fecha', required=False),
		'fecha': fields.char('Fecha:', readonly=False,  required=False),
		'tipo_envio' : fields.selection((('Interno','Interno'), ('Externo','Externo')),'Tipo de Envio', required=False),
	}
	_defaults = {
		'f_correlativo': lambda *a: time.strftime("%Y"),
		'fecha': lambda *a: time.strftime("%d-%m-%Y"),
		'correlativo' : _gen_correlativo,
	}
def acento(cadena):
	result = cadena.encode('UTF-8').decode('UTF-8')# INSTITUCION
	return result
movimientos_gba()
def addComa( snum ):
	"Adicionar comas como separadores de miles a n. n debe ser de tipo string"
	s = snum;
	i = s.index('.') # Se busca la posición del punto decimal
	while i > 3:
	    i = i - 3
	    s = s[:i] +  '#' + s[i:]
	    
	n = s.replace(".", ",", 5);
	t = n.replace("#", ".", 5);
	
	