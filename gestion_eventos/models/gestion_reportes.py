# -*- coding: utf-8 -*-

#import time # Necesario para las funciones de Fecha
import pdf_class # Se importa la Clase constructora del Documento PDF

from openerp.osv import osv, fields

class Gestion_reportes(osv.Model):
	_name="gestion.reportes"

	_order = 'cantidad'
	
	_rec_name = 'cantidad'
	#################################################################
	# METODO PARA GERAR LOS DIFERENTES REPORTES DE GESTION DE EVENTOS
	#################################################################

	def gestion_emitir_detallado(self, cr, uid, ids, context=None):
		# Instancia de la clase heredada L es horizontal y P es vertical

		# REALIZAMOS LA LECTURA DE LOS VALORES A FILTRAR
		for gestion in self.browse(cr, uid, ids, context=None):
			cantidad = gestion.cantidad
			mostrar  = gestion.asc_desc

		cr.execute('SELECT ge.name FROM gestion_eventos AS g ,gestion_inst_gerencia AS ge WHERE g.institucion=ge.id ORDER BY status '+str(mostrar)+' LIMIT '+str(cantidad)+'')

		for detallado in cr.fetchall():

			print "INSTITUCION: "+str(detallado[0].encode('UTF-8'))
			# print "ACTIVIDAD: "+str(detallado[19])

		pdf=pdf_class.Detallado(orientation='P',unit='mm',format='letter') #HORIENTACION DE LA PAGINA

		pdf.set_author('ING JESUS LAYA')
		pdf.alias_nb_pages() # LLAMADA DE PAGINACION
		pdf.add_page() # AÑADE UNA NUEVA PAGINACION
		#pdf.set_font('Times','',10) # TAMANO DE LA FUENTE
		pdf.set_font('Arial','B',15)
		pdf.set_fill_color(157,188,201) # COLOR DE BOLDE DE LA CELDA
		pdf.set_text_color(24,29,31) # COLOR DEL TEXTO

		pdf.ln(7)

		pdf.set_fill_color(199,15,15)
		pdf.set_text_color(255,255,255)
		pdf.set_font('Arial','B',10)
		pdf.cell(190,5,"DIRECCIÓN DEL EVENTO".decode("UTF-8"),'LTBR',1,'C',1)
		pdf.set_fill_color(255,255,255)
		pdf.set_text_color(24,29,31)
		pdf.set_font('Arial','B',9)
		pdf.cell(70,5,"Municipio:".decode("UTF-8"),'LTB',0,'L',1)
		pdf.cell(70,5,"Parroquia:".decode("UTF-8"),'LTB',0,'L',1)
		pdf.cell(40,5,"Fecha:".decode("UTF-8"),'LTB',0,'L',1)
		pdf.set_font('Arial','',8)
		pdf.cell(10,5,"".decode("UTF-8"),'BTR',1,'L',1)
		pdf.set_font('Arial','B',9)
		pdf.cell(147,5,"Dirección:".decode("UTF-8"),'LTB',0,'L',1)
		pdf.set_font('Arial','',8)
		pdf.set_font('Arial','B',9)
		pdf.set_font('Arial','',8)
		pdf.cell(43,5,"".decode("UTF-8"),'TBR',1,'L',1)

		pdf.set_font('Arial','B',9)

		pdf.ln(5)
		pdf.set_fill_color(199,15,15)
		pdf.set_text_color(255,255,255)
		pdf.set_font('Arial','B',10)

		pdf.cell(190,5,"CARACTERISTICA DEL EVENTO".decode("UTF-8"),'LTBR',1,'C',1)

		pdf.set_fill_color(255,255,255)
		pdf.set_text_color(24,29,31)
		pdf.set_font('Arial','b',8)

		pdf.cell(160,5,"Actividad".decode("UTF-8"),'LTBR',0,'L',1)
		pdf.cell(30,5,"Participantes:".decode("UTF-8"),'LTBR',1,'L',1)

		pdf.cell(190,10,"TEXTO".decode("UTF-8"),'LTBR',1,'L',1)

		pdf.cell(100,10,"Institución / Gerencia:".decode("UTF-8"),'LTBR',0,'L',1)
		pdf.cell(60,10,"Responsable:".decode("UTF-8"),'LTBR',0,'L',1)
		pdf.cell(30,10,"Estátus:".decode("UTF-8"),'LTBR',1,'L',1)

		########################################################################
		#          CONSTRUCCION DE LA LEYENDA DE LOS TIPOS DE EVENTOS
		########################################################################
		pdf.set_fill_color(199,15,15)
		pdf.set_text_color(255,255,255)
		pdf.ln(5)
		pdf.cell(60,5,"TOTAL ACTIVIDADES".decode("UTF-8"),'LTBR',0,'C',1)

		pdf.ln(5)
		pdf.set_font('Arial','',8)
		pdf.set_text_color(0,0,0)
		pdf.set_fill_color(255,255,255)
		pdf.cell(20,4,"Cantidad".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(40,4,"Eventos".decode("UTF-8"),'LTBR',1,'C',1)

		# Pendientes
		pdf.cell(20,4,"Cantidad A:".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(40,4,"Pendientes".decode("UTF-8"),'LTBR',1,'C',1)
		# Realizadas
		pdf.cell(20,4,"Cantidad B:".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(40,4,"Realizados".decode("UTF-8"),'LTBR',1,'C',1)
		# Postpuestos
		pdf.cell(20,4,"Cantidad C:".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(40,4,"Postpuestos".decode("UTF-8"),'LTBR',1,'C',1)
		# Reprogramado
		pdf.cell(20,4,"Cantidad D:".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(40,4,"Reprogramados".decode("UTF-8"),'LTBR',1,'C',1)
		# Atrasado
		pdf.cell(20,4,"Cantidad E:".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(40,4,"Atrasados".decode("UTF-8"),'LTBR',1,'C',1)
		# Cancelado
		pdf.cell(20,4,"Cantidad BD:".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(40,4,"Cancelados".decode("UTF-8"),'LTBR',1,'C',1)

		########################################################################
		pdf.ln(5)
		pdf.set_x(100)
		pdf.set_fill_color(199,15,15)
		pdf.set_text_color(255,255,255)
		pdf.set_font('Arial','B',10)

		pdf.output('openerp/addons/gestion_eventos/reportes/Gestión de Eventos.pdf','F')

	#################################################################
	_columns = {

		'cantidad': fields.char(string="Cantidad", required = True),
		'asc_desc' : fields.selection([('asc','Asendente'),('desc','Decendente')], string="", required=True),
	}

	_defaults = {
		#'codigo' : 
	}



