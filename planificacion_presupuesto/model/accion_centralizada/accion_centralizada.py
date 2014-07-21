# -*- coding: utf-8 -*-
import hashlib
import itertools
import logging
import os
import re
import class_pdf
import base64
import random
import unicodedata
from openerp import tools
from openerp.osv import fields,osv
from openerp import SUPERUSER_ID

_logger = logging.getLogger(__name__)
import time
import random
from time import gmtime, strftime
from openerp.osv import osv, fields
from datetime import datetime, timedelta
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring #Necesario para la generación del .xsl
import netsvc
import tools
import logging
import xlwt
from xlwt import Workbook
from xlwt import Font
from xlwt import XFStyle
from xlwt import Borders
import os
import math
import re
import unicodedata
import base64 #Necesario para la generación del .xls

# Clase Solicitud de reparacion de Canaima
class accion_centralizada(osv.Model):

    #  Nombre del objeto
    _name = "accion.centralizada"

    _order = 'c_solicitud'
    _rec_name = 'c_solicitud'

    """
    Metodo que genera el codigo se solicitud donde se busca el ultimo valor encontrado en la BD
    y se le suma 1.
    """
    def _get_last_id(self, cr, uid, ids, context = None):

	sfl_id       = self.pool.get('accion.centralizada')
	srch_id      = sfl_id.search(cr,uid,[])
        rd_id        = sfl_id.read(cr, uid, srch_id, context=context)
        if rd_id:
            id_documento = rd_id[-1]['c_solicitud']
            c_nota = id_documento[:]
            last_id      = c_nota.lstrip('0')
            str_number   = str(int(last_id) + 1)
            last_id      = str_number.rjust(5,'0')
            codigo      = last_id
        else :
            str_number = '1'
            last_id      = str_number.rjust(5,'0')
            codigo      = last_id
        return codigo
	
    """
    Funcion para eliminar las tildes de algun texto utilizando el modulo unicodedata.
    """
    def elimina_tildes(self, s):
    
        return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

    """
    Metodo que trae la informacion de cada Ente/Organizacion.
    """
    def on_change_ente(self, cr, uid, ids, organismo, context=None):
        values = {}
        if not organismo:
            return values
        datos = self.pool.get('organos.entes').browse(cr, uid, organismo, context=context)
        values.update({
            'domicilio' : datos.direccion,
            'n_autoridad' : datos.nom_responsable,
            'cargo' : datos.cargo,
            'telefono': datos.telefono,
            'correo': datos.correo,
	    'cedula': datos.ci,
	    'siglas': datos.siglas,
     
        })
        return {'value' : values}  



    def vincular_partida(self, cr, uid, ids, context=None):
		
		browse_id = self.browse(cr, uid, ids, context=None) #Lectura del propio objeto (Registro)
		
		for x in browse_id:
			id_centralizada = x.n_accion_centra.id
			id_model        = x.id
		
		partida = self.pool.get('partida.centralizada') # Objeto hr_employee (Empleado)
		
		search_p = partida.search(cr, uid, [('a_centralizada','=',id_centralizada)], context=None) # Se busca el ID dado
		par      = partida.read(cr,uid,search_p,context=context) # Se refleja el resultado
		
		for p in par:

			cod     = p['codigo']
			partida =  p['partida'][0]

			centralizada = self.pool.get('imputacion.accion.centralizada') # Objeto hr_employee (Empleado)
			search_c = centralizada.search(cr, uid, [('imputacion_acc_ids','=',id_model),('codigo','=',cod)], context=None) # Se busca el ID dado
			
			print "CENTRALIZADA EXISTE: "+str(search_c)

			if not search_c:
			
				cod     = p['codigo']
				partida =  p['partida'][0]
				
				self.pool.get('imputacion.accion.centralizada').create(cr, uid, {
					'imputacion_acc_ids': id_model,
					'partida_presu': partida,
					'codigo': cod,
				}, context=context)



    """
    Metodo que trae la informacion de cada Ente/Organizacion.
    """
    def on_change_acciones_especificas(self, cr, uid, ids, n_accion_centra, context=None):
        values = {}
        if not n_accion_centra:
            return values
	print n_accion_centra
        datos = self.pool.get('tipo.accion.especifica')
	datos_acciones = datos.search(cr, uid, [('a_centralizada','=',n_accion_centra)], context=None)
	especificas = datos.read(cr,uid,datos_acciones,context=context)
	acc_espe = ""
	for k in especificas:
	    acc_espec = k['a_especifica'].encode("UTF-8").decode("UTF-8")+"\n"
	    acc_espe = acc_espe + acc_espec
	values.update({
	    'n_accion_espe' : acc_espe,
     
	})
        return {'value' : values}  


        """
    Metodo con el cual genero el archivo .pdf 
    """

    def reporte_acciones(self, cr, uid, ids, context=None): # Generacion de inventario

        # Instancia de la clase heredada L es horizontal y P es vertical
        # format A4, A3 o letter que son los formatos de la hoja (oficio, carta, etc)

        pdf=class_pdf.PDF(orientation='P',unit='mm',format='letter') #HORIENTACION DE LA PAGINA
        
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
        accion_centra = self.browse(cr, uid, ids, context=context)
        npro = ""
        amb = ""
        for y in accion_centra:
	    c_id = y.c_solicitud
            ente = y.organismo.nombre_ente.encode("UTF-8").decode("UTF-8")
            fec = y.f_solicitud.encode("UTF-8").decode("UTF-8")
            ci = y.cedula.encode("UTF-8").decode("UTF-8")
            autori = y.n_autoridad.encode("UTF-8").decode("UTF-8")
            cargo = y.cargo.encode("UTF-8").decode("UTF-8")
	    sigla = y.siglas.encode("UTF-8").decode("UTF-8")
            tel = y.telefono.encode("UTF-8").decode("UTF-8")
            email = y.correo.encode("UTF-8").decode("UTF-8")
            politica = y.poli_presu.encode("UTF-8").decode("UTF-8")
            
            acc_central = y.n_accion_centra.a_centralizada.encode("UTF-8").decode("UTF-8")
            acc_espe = y.n_accion_espe.encode("UTF-8").decode("UTF-8")

            
            pdf.ln(13)
            pdf.set_fill_color(199,15,15)
            pdf.set_text_color(255,255,255)
            pdf.set_font('Arial','B',10)
            pdf.cell(190,5,"1. IDENTIFICACIÓN DEL PROPONENTE".decode("UTF-8"),'LTBR',1,'C',1)
            pdf.set_fill_color(255,255,255)
            pdf.set_text_color(24,29,31)
            
            pdf.set_font('Arial','B',9)
            pdf.cell(47,5,"1.1 Organismo/Ente/Empresa:".decode("UTF-8"),'LTB',0,'L',1)
            pdf.set_font('Arial','',8)
            pdf.cell(143,5,ente,'BTR',1,'L',1)
            pdf.set_font('Arial','B',9)
            pdf.cell(82,5,"1.2. Nombre de la Máxima Autoridad de la Institución:".decode("UTF-8"),'LTB',0,'L',1)
            pdf.set_font('Arial','',8)
            pdf.cell(70,5,autori,'TBR',0,'L',1)
            pdf.set_font('Arial','B',9)
            pdf.cell(13,5,"1.3. C.I.:".decode("UTF-8"),'LTB',0,'L',1)
            pdf.set_font('Arial','',8)
            pdf.cell(25,5,ci,'TBR',1,'L',1)
            pdf.set_font('Arial','B',9)
            pdf.cell(18,5,"1.4. Cargo:".decode("UTF-8"),'LTB',0,'L',1)
            pdf.set_font('Arial','',8)
            pdf.cell(48,5,cargo,'BTR',0,'L',1)
            pdf.set_font('Arial','B',9)
            pdf.cell(37,5,"1.5. Correo Electrónico:".decode("UTF-8"),'LTB',0,'L',1)
            pdf.set_font('Arial','',7)
            pdf.cell(45,5,email,'BTR',0,'L',1)
            pdf.set_font('Arial','B',9)
            pdf.cell(22,5,"1.6. Teléfono:".decode("UTF-8"),'LTB',0,'L',1)
            pdf.set_font('Arial','',8)
            pdf.cell(20,5,tel,'TBR',1,'L',1)

            pdf.set_fill_color(199,15,15)
            pdf.set_text_color(255,255,255)
            pdf.set_font('Arial','B',10)
            pdf.cell(190,5,"2. POLÍTICA PRESUPUESTARÍA".decode("UTF-8"),'LTBR',1,'C',1)
            pdf.set_fill_color(255,255,255)
            pdf.set_text_color(24,29,31)
            pdf.set_font('Arial','',8)
            pdf.multi_cell(190,5,politica,'LTBR','J',0)

            pdf.set_fill_color(199,15,15)
            pdf.set_text_color(255,255,255)
            pdf.set_font('Arial','B',10)
            pdf.cell(190,5,"3. DATOS BÁSICOS DE LA ACCIÓN CENTRALIZADA".decode("UTF-8"),'LTBR',1,'C',1)
            pdf.cell(190,5,"3.1. ACCIÓN CENTRALIZADA".decode("UTF-8"),'LTBR',1,'C',1)
            pdf.set_fill_color(255,255,255)
            pdf.set_text_color(24,29,31)
            pdf.set_font('Arial','B',9)
            
            pdf.cell(60,5,"3.1. Nombre de la Acción Centralizada:".decode("UTF-8"),'LTB',0,'L',1)
            pdf.set_font('Arial','',8)
            pdf.cell(130,5,acc_central,'BTR',1,'L',1)
            pdf.set_font('Arial','B',9)
            pdf.cell(190,5,"3.2. Nombre de la Acción Especifíca:".decode("UTF-8"),'LTRR',1,'L',1)
            pdf.set_font('Arial','',8)
	    pdf.multi_cell(190,4,acc_espe,'LBR',0,'J',0)

	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"4. ACTIVIDADES DE LA ACCIÓN ESPECÍFICA".decode("UTF-8"),'LTBR',1,'C',1)
	    pdf.cell(190,5,"4.1. Distribución de las Actividades".decode("UTF-8"),'LTBR',1,'C',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(54,5,"Actividades".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.cell(35, 5,"Unidad de Medida".decode("UTF-8"),'LTB',0,'C',1)
	    pdf.cell(40, 5,"Medio de Verificación".decode("UTF-8"),'LTB',0,'C',1)
	    pdf.cell(16,5,"Cantidad".decode("UTF-8"),'LBTR',0,'C',1)
	    pdf.cell(45, 5,"Indicadores de la Actividad".decode("UTF-8"),'LTBR',1,'C',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)
	    
	    dist_ids = self.read(cr, uid, ids, context=context)[0]
	    dis_id = dist_ids['distribucion_actividades'] # Grupo de IDS

	    dis_act = self.pool.get('distribucion.actividades') # Objeto 
	    act_distri = dis_act.search(cr, uid, [('id','=',dis_id)], context=None)
	    distribucion = dis_act.read(cr,uid,act_distri,context=context)

    
	    for d in distribucion:
		act = d['actividades']
		unid = d['unidad_medida']
		medio = d['medio_verifi']
		cant = int(d['cantidad'])
		indi = d['indicadores_act']

		pdf.set_font('Arial','',6)
		pdf.cell(54,5, act.encode("UTF-8").decode("UTF-8"),'LTB',0,'J',0),
		pdf.cell(35, 5, unid.encode("UTF-8").decode("UTF-8"),'LTB',0,'C',1)
		pdf.cell(40, 5, medio.encode("UTF-8").decode("UTF-8"),'LTB',0,'C',1)
		pdf.cell(16,5, str(cant),'LBTR',0,'C',1)
		pdf.cell(45, 5, indi.encode("UTF-8").decode("UTF-8"),'LTBR',1,'C',1)

	    
	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"4.2. Distribución Trimestral de las Actividades".decode("UTF-8"),'LTBR',1,'C',1)
	    
	    
	    pdf.set_font('Arial','B',9)
	    pdf.cell(54,5,"Actividades".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.cell(29, 5,"I Trimestre".decode("UTF-8"),'LTB',0,'C',1)
	    pdf.cell(29, 5,"II Trimestre".decode("UTF-8"),'LTB',0,'C',1)
	    pdf.cell(29, 5,"III Trimestre".decode("UTF-8"),'LTB',0,'C',1)
	    pdf.cell(29, 5,"IV Trimestre".decode("UTF-8"),'LTB',0,'C',1)
	    pdf.cell(20,5,"TOTAL".decode("UTF-8"),'LBTR',1,'C',1) 
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)
	    
	    acti_ids = self.read(cr, uid, ids, context=context)[0]
	    act_id = acti_ids['actividades_trimestrales'] # Grupo de IDS

	    act_trim = self.pool.get('actividades.trimestrales') # Objeto 
	    act_trimestrales = act_trim.search(cr, uid, [('id','=',act_id)], context=None)
	    actividades = act_trim.read(cr,uid,act_trimestrales,context=context)

    
	    for a in actividades:
		act = a['actividades']
		uno = int(a['trim_1'])
		dos = int(a['trim_2'])
		tres = int(a['trim_3'])
		cuatro = int(a['trim_4'])
		total_trim = int(a['total_trim'])
		
		pdf.set_font('Arial','',6)
		pdf.cell(54,5, act.encode("UTF-8").decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(29, 5, str(uno),'LTB',0,'C',1)
		pdf.cell(29, 5, str(dos),'LTB',0,'C',1)
		pdf.cell(29, 5, str(tres),'LTB',0,'C',1)
		pdf.cell(29, 5, str(cuatro),'LTB',0,'C',1)
		pdf.cell(20,5, str(total_trim),'LBTR',1,'C',1) 

	    pdf.set_font('Arial','B',9)
	    pdf.cell(170, 5, "TOTALES",'LTB',0,'C',1)
	    pdf.cell(20,5, "",'LBTR',1,'C',1) 
	    
	    
	    pdf.alias_nb_pages() # LLAMADA DE PAGINACION
	    pdf.add_page() # AÑADE UNA NUEVA PAGINACIO
	    pdf.set_y(43)
	    pdf.set_x(10)
	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"5. METAS FINANCIERAS DE LAS ACCIÓN ESPECÍFICA".decode("UTF-8"),'LTBR',1,'C',1)
	    pdf.cell(190,5,"5.1. Distribución Trimestral".decode("UTF-8"),'LTBR',1,'C',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(54,5,"Actividades".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.cell(29, 5,"I Trimestre".decode("UTF-8"),'LTB',0,'C',1)
	    pdf.cell(29, 5,"II Trimestre".decode("UTF-8"),'LTB',0,'C',1)
	    pdf.cell(29, 5,"III Trimestre".decode("UTF-8"),'LTB',0,'C',1)
	    pdf.cell(29, 5,"IV Trimestre".decode("UTF-8"),'LTB',0,'C',1)
	    pdf.cell(20,5,"TOTAL".decode("UTF-8"),'LBTR',1,'C',1)   
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)
	    
	    meta_ids = self.read(cr, uid, ids, context=context)[0]
	    meta_acc_id = meta_ids['meta_acc_esp_trim'] # Grupo de IDS

	    meta_especi = self.pool.get('metas.especificas') # Objeto 
	    m_esp = meta_especi.search(cr, uid, [('id','=',meta_acc_id)], context=None)
	    metas = meta_especi.read(cr,uid,m_esp,context=context)

    
	    for m in metas:
		act = m['actividades']
		uno = float(m['trim_1'])
		dos = float(m['trim_2'])
		tres = float(m['trim_3'])
		cuatro = float(m['trim_4'])
		total_m = float(m['total_trim'])

		pdf.set_font('Arial','',6)
		pdf.cell(54,4,act.encode("UTF-8").decode("UTF-8"),'LTBR',0,'L',1)
		pdf.cell(29,4,str(uno),'LTBR',0,'R',1)
		pdf.cell(29,4,str(dos),'LTBR',0,'R',1)
		pdf.cell(29,4,str(tres),'LTBR',0,'R',1)
		pdf.cell(29,4,str(cuatro),'LTBR',0,'R',1)
		pdf.cell(20,4,str(total_m),'LTBR',1,'R',1) 

	    pdf.set_font('Arial','B',9)
	    pdf.cell(170, 5, "TOTALES",'LTB',0,'C',1)
	    pdf.cell(20,5, "",'LBTR',1,'C',1) 
	    
	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"6. IMPUTACIÓN ACCIONES".decode("UTF-8"),'LTBR',1,'C',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)
	    
	    pdf.set_font('Arial','B',9)
	    pdf.cell(20,4,"Código".decode("UTF-8"),'LTR',0,'L',1)
	    pdf.cell(82,4,"Partida Presupuestaria".decode("UTF-8"),'LTR',0,'L',1)
	    pdf.cell(68,4,"Distribución Trimestral".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.cell(20,4,"Total".decode("UTF-8"),'LTR',1,'C',1)
	    pdf.set_font('Arial','',9)
	    pdf.cell(20,4,"",'LBR',0,'L',1)
	    pdf.cell(82,4,"",'LBR',0,'L',1)
	    pdf.cell(17,4,"I".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.cell(17,4,"II".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.cell(17,4,"III".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.cell(17,4,"IV".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(20,4,"",'LBR',1,'C',1)
	    
	impu_ids = self.read(cr, uid, ids, context=context)[0]
	imp_id = impu_ids['imputacion_acciones'] # Grupo de IDS

	imp_pre = self.pool.get('imputacion.accion.centralizada') # Objeto 
	imputa = imp_pre.search(cr, uid, [('id','=',imp_id)], context=None)
	impu_acciones = imp_pre.read(cr,uid,imputa,context=context)
	    

	for f in impu_acciones:
	    codi = f['codigo']
	    partida = f['partida_presu'][1]
	    tri_uno = float(f['trim_1'])
	    tri_dos = float(f['trim_2'])
	    tri_tres = float(f['trim_3'])
	    tri_cuatro = float(f['trim_4'])
	    tri_total_i = float(f['total_impu'])


	    
	    pdf.set_font('Arial','',6)
	    pdf.cell(20,4,str(codi),'LTBR',0,'L',1)
	    pdf.cell(82,4,partida.encode("UTF-8").decode("UTF-8"),'LTBR',0,'L',1)
	    pdf.cell(17,4,str(tri_uno),'LTBR',0,'R',1)
	    pdf.cell(17,4,str(tri_dos),'LTBR',0,'R',1)
	    pdf.cell(17,4,str(tri_tres),'LTBR',0,'R',1)
	    pdf.cell(17,4,str(tri_cuatro),'LTBR',0,'R',1)
	    pdf.cell(20,4,str(tri_total_i),'LTBR',1,'R',1)
	
	pdf.set_font('Arial','B',9)
	pdf.cell(102,4,"Totales",'LTBR',0,'C',1)
	pdf.cell(17,4,"",'LTBR',0,'R',1)
	pdf.cell(17,4,"",'LTBR',0,'R',1)
	pdf.cell(17,4,"",'LTBR',0,'R',1)
	pdf.cell(17,4,"",'LTBR',0,'R',1)
	pdf.cell(20,4,"",'LTBR',1,'R',1)   


	nom = c_id+"-"+sigla+'.pdf'
        pdf.output('/home/administrador/openerp70/modules/planificacion_presupuesto/reportes/'+nom,'F')

        #archivo = open('openerp/addons/planificacion_presupuesto/reportes/'+nom)
	archivo = open('/home/administrador/openerp70/modules/planificacion_presupuesto/reportes/'+nom)
	r_archivo = self.pool.get('reportes.presupuesto').create(cr, uid, {
		'name' : nom,
		'res_name' : nom,
		'datas' : base64.encodestring(archivo.read()),
		'datas_fname' : nom,
		'res_model' : 'accion.centralizada',
		'registro': 'Accion Centralizada',
		},context=context)
	
	return r_archivo
	
	

    _columns = {
	'estatus': fields.selection([('1','Revisando'), ('2','Rechazado'), ('3','Para Ajuste'), ('4','Aprobado')], string="Estatus"),
        'c_solicitud' : fields.char(string="ID", size=255, required=True, readonly=True),
	'user_register': fields.many2one('res.users', 'Registrado por:', readonly=True),
	'f_solicitud': fields.char('Fecha de Elaboración:', required=True, readonly=True),
	#Pestaña1
	'organismo': fields.many2one('organos.entes', 'Organismo/Ente/Empresa:', required=True),
        'n_autoridad': fields.char('Nombre de la Máxima Autoridad de la Institución:', required=True),
	'cedula': fields.char('C.I.:', required=True),
	'cargo': fields.char('Cargo:', required=True),
	'telefono': fields.char('Teléfono:', required=True),
	'correo': fields.char('Correo Electrónico:', required=True),
	'siglas': fields.char('Siglas:'),
	#Pestaña2
	'poli_presu': fields.text('Política Presupuestaría:', required=True),
	#Pestaña3
	'n_accion_centra': fields.many2one('tipo.accion.centralizada', 'Nombre de la Acción Centralizada', required=True),
	'n_accion_espe': fields.text("Acciones Específicas", required=True),
	#'n_accion_espe': fields.many2one('tipo.accion.especifica', 'Nombre de la Acción Específica', required=True),
	#pestaña4
	'distribucion_actividades':fields.one2many('distribucion.actividades', 'distribucion_ids',required=False),
	#pestaña5
	'actividades_trimestrales':fields.one2many('actividades.trimestrales', 'act_trimestral_ids',required=False),
	'total_actividades':fields.integer(string="Cant. total", required=False), #Nuevo
	#pestañas6
	'meta_acc_esp_trim':fields.one2many('metas.especificas', 'metas_acc_espec',required=False),
	'total_metas':fields.float(string="Cant. total", required=False), #Nuevo
	#pestaña 7
	'imputacion_acciones':fields.one2many('imputacion.accion.centralizada', 'imputacion_acc_ids',required=False),
	'total_imputaciones':fields.float(string="Cant. total", required=False), #Nuevo
	#Pestaña Observaciones
	'revisado': fields.char('Revisado por:', readonly=True, required=False),
	'fecha_revision': fields.char('Fecha de Revisión:', readonly=True, required=False),
	'partida01': fields.float(string="4.01", size=10, readonly=True, required=False),
	'partida02': fields.float(string="4.02", size=10, readonly=True, required=False),
	'partida03': fields.float(string="4.03", size=10, readonly=True, required=False),
	'partida04': fields.float(string="4.04", size=10, readonly=True, required=False),
	'partida05': fields.float(string="4.05", size=10, readonly=True, required=False),
	'partida07': fields.float(string="4.07", size=10, readonly=True, required=False),
	'partida10': fields.float(string="4.10", size=10, readonly=True, required=False),
	'partida11': fields.float(string="4.11", size=10, readonly=True, required=False),
	'partida12': fields.float(string="4.12", size=10, readonly=True, required=False),
	'observaciones': fields.text('Observaciones:', readonly=True, required=False),
	'monto_asignado': fields.float(string="Monto Asignado", readonly=True, required=False),
        }

    _defaults = {
        'f_solicitud': lambda *a: time.strftime("%d/%m/%Y"),
        'c_solicitud': _get_last_id,
        'user_register': lambda s, cr, uid, c: uid,
	'estatus': '1',
  
    }     

    #Método para copiar las actividades de la pestaña de 'Actividades específicas' a las pestañas de 'Distribución trimestral' y 'Metas específicas'
    def carga_actividades(self, cr, uid, ids, context=None):
			values = {}
			#Modelos a escribir
			dis_tri = self.pool.get('actividades.trimestrales')
			metas_tri = self.pool.get('metas.especificas')
			
			#Modelo actual
			browse_id = self.browse(cr, uid, ids, context=context)
			
			id_act = ""
			id_metas = ""
			id_accion = 0
			for accion in browse_id:
				id_accion = accion.id
				
				activ = ""
				r = False
				i = 1 
				for actividad in accion.distribucion_actividades:
					#~ print "Actividad"+str(i)+": "+str(actividad.actividades)
					
					if actividad.actividades:	
						activ = actividad.actividades.encode('UTF-8')
						
						#Verificamos si ya existen las actividades en los modelos correspondiente
						buscar_act = dis_tri.search(cr, uid, [('act_trimestral_ids','=',id_accion),('actividades','=',activ)], count=False)
						buscar_m = metas_tri.search(cr, uid, [('metas_acc_espec','=',id_accion),('actividades','=',activ)], count=False)
						
						#Carga de las actividades	en los modelos correspondientes
						if not buscar_act:
							id_act = dis_tri.create(cr, uid, {
								'act_trimestral_ids' : id_accion,
								'actividades' : activ,
							},context=context)
						
						if not buscar_m:
							id_metas = metas_tri.create(cr, uid, {
								'metas_acc_espec' : id_accion,
								'actividades' : activ,
							},context=context)
						
						if id_act and id_metas:
							r = True
					
					#Aumento del contador
					i = i + 1
				
			return r
			
    
    #Método para el cálculo del monto total de las metas----------------------------------------------------------
    def total_metas(self, cr, uid, ids, metas, context=None):

	values = {}
	
	cantidad_meta_m = 0
	
	cantidad_meta_v = 0
	
	total_metas = 0

	browse_id = self.browse(cr, uid, ids, context=context)
	
	#Segmento que obtiene los montos directamente del modelo
	i = 0
	for proyecto in browse_id:
	    i = 0
	    for meta in proyecto.meta_acc_esp_trim:
		cantidad_meta_m = meta.total_trim
		total_metas = total_metas + cantidad_meta_m
	    i = i + 1
		
	#Segmento que obtiene los montos directamente de la vista
	j = 0
	for mt in metas:
	    if not mt[2]:
		cantidad_meta_v = 0
		total_metas = total_metas + cantidad_meta_v
	    else:
				claves = mt[2].keys() #Variable que obtiene las claves del diccionario
				#Verificamos si existe la clave 'total'
				n_c = 0 #Contador de clave
				for clv in claves:
					if clv == 'total_trim':
						n_c = n_c + 1
						
				if n_c > 0:				
					cantidad_meta_v = mt[2]['total_trim']
					total_metas = total_metas + cantidad_meta_v
					
					for meta2 in proyecto.meta_acc_esp_trim:
						if meta2.id == mt[1] and mt[2] != False:
							total_metas = total_metas - meta2.total_trim
		    
	    j = j + 1
	
	values.update({
	    'total_metas' : total_metas,
	})
	
	return {'value':values}
				
				
    #~ Método para el cálculo del monto total de las imputaciones presupuestarias________________________________________________________________________________
    def total_imputaciones(self, cr, uid, ids, imputaciones, context=None):
			
	values = {}
	
	cantidad_imp_m = 0
	
	cantidad_imp_v = 0
	
	total_imputaciones = 0

	browse_id = self.browse(cr, uid, ids, context=context)
	
	#Segmento que obtiene los montos directamente del modelo
	i = 0
	for proyecto in browse_id:
	    i = 0
	    for imputacion in proyecto.imputacion_acciones:
		cantidad_imp_m = imputacion.total_impu
		total_imputaciones = total_imputaciones + cantidad_imp_m

	    i = i + 1
		
	#Segmento que obtiene los montos directamente de la vista
	j = 0
	for imp in imputaciones:
	    if not imp[2]:
		cantidad_imp_v = 0
		total_imputaciones = total_imputaciones + cantidad_imp_v
	    else:
				claves = imp[2].keys() #Variable que obtiene las claves del diccionario
				#Verificamos si existe la clave 'total'
				n_c = 0 #Contador de clave
				for clv in claves:
					if clv == 'total_impu':
						n_c = n_c + 1
		
				if n_c > 0:				
					cantidad_imp_v = imp[2]['total_impu']
					total_imputaciones = total_imputaciones + cantidad_imp_v  
					
					for imputacion2 in proyecto.imputacion_acciones:
						if imputacion2.id == imp[1] and imp[2] != False:
							total_imputaciones = total_imputaciones - imputacion2.total_impu
					
	    j = j + 1
	
	values.update({
	    'total_imputaciones' : total_imputaciones,
	})
	
	return {'value':values}
				
				
    #~ Método para el cálculo de la cantidad total de actividades---------------------------------------------------------------
    def total_actividades(self, cr, uid, ids, actividades, context=None):
			
	values = {}
	
	cantidad_act_m = 0
	
	cantidad_act_v = 0
	
	total_actividades = 0

	browse_id = self.browse(cr, uid, ids, context=context)
	
	#Segmento que obtiene los montos directamente del modelo
	i = 0
	for proyecto in browse_id:
	    i = 0
	    for actividad in proyecto.actividades_trimestrales:
		cantidad_act_m = actividad.total_trim
		total_actividades = total_actividades + cantidad_act_m
	    i = i + 1
		
	#Segmento que obtiene los montos directamente de la vista
	j = 0
	for act in actividades:
	    if not act[2]:

		cantidad_act_v = 0
		total_actividades = total_actividades + cantidad_act_v
	    else:
				claves = act[2].keys() #Variable que obtiene las claves del diccionario
				#Verificamos si existe la clave 'total'
				n_c = 0 #Contador de clave
				for clv in claves:
					if clv == 'total_trim':
						n_c = n_c + 1
		
				if n_c > 0:				
					#~ print act[2]['total_trim']
					cantidad_act_v = act[2]['total_trim']
					total_actividades = total_actividades + cantidad_act_v
					
					for actividad2 in proyecto.actividades_trimestrales:
						if actividad2.id == act[1] and act[2] != False:
							total_actividades = total_actividades - actividad2.total_trim
		    
	    j = j + 1
	
	values.update({
	    'total_actividades' : total_actividades,
	})
	
	return {'value':values}
