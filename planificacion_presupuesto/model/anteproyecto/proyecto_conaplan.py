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
class solicitud_soporte(osv.Model):

    #  Nombre del objeto
    _name = "proyecto.conaplan"

    _order = 'c_solicitud'
    _rec_name = 'c_solicitud'


    """
    Metodo que genera el codigo se solicitud donde se busca el ultimo valor encontrado en la BD
    y se le suma 1.
    """
    def _get_last_id(self, cr, uid, ids, context = None):

	    sfl_id       = self.pool.get('proyecto.conaplan')
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
    def on_change_entes(self, cr, uid, ids, organismo, context=None):
        values = {}
        if not organismo:
            return values
        datos = self.pool.get('organos.entes').browse(cr, uid, organismo, context=context)
        values.update({
            'domicilio' : datos.direccion,
            'responsable' : datos.nom_responsable,
            'cargo' : datos.cargo,
            'telefono': datos.telefono,
            'correo': datos.correo,
	    'ubicacion': datos.direccion,
	    'siglas': datos.siglas,

        })
        return {'value' : values}    

    def on_change_total(self, cr, uid, ids, bene_femenino, bene_masculino, context=None):

        values = {}
        total = int(bene_femenino) + int(bene_masculino)
        values.update({'bene_total' : total,})
        return {'value' : values} 

    def on_change_total_estimado(self, cr, uid, ids, empleos_directos_f, empleos_directos_m, context=None):

        values = {}
        est_total = int(empleos_directos_f) + int(empleos_directos_m)
        values.update({'t_emple_directos' : est_total,})
        return {'value' : values} 



    """
    Metodo con el cual genero el archivo .pdf 
    """

    def reporte_anteproyecto(self, cr, uid, ids, context=None): # Generacion de inventario

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
	proyect = self.browse(cr, uid, ids, context=context)
	npro = ""
	amb = ""
	fuente_f = ""
	exp_r = ""
	exp_c = ""
	int_r = ""
	int_c = ""
	obj_g = ""
	conf_int = ""
	conf_exp = ""
	emp_dir_f = 0
	emp_dir_m = 0
	bene_f = 0
	bene_m = 0
	for x in proyect:
	    ente = x.organismo.nombre_ente.encode("UTF-8").decode("UTF-8")
	    fec = x.f_solicitud
	    domici = x.domicilio.encode("UTF-8").decode("UTF-8")
	    resp = x.responsable.encode("UTF-8").decode("UTF-8")
	    cargo = x.cargo.encode("UTF-8").decode("UTF-8")
	    tel = x.telefono.encode("UTF-8").decode("UTF-8")
	    correo = x.correo.encode("UTF-8").decode("UTF-8")
	    
	    proyecto = x.nombre_pro.encode("UTF-8").decode("UTF-8")
	    dura = x.duracion.encode("UTF-8").decode("UTF-8")
	    inicio = x.fecha_ini_fin.encode("UTF-8").decode("UTF-8")
	    fin = int(x.year_fiscal)
	    ###########################
	    if int(x.etapa) == 1:
		etapa = "Nueva"
	    else:
		etapa = "Continuación"
	    ###########################
	    if x.proy_nuevo == False:
		npro = ""
	    else:
		npro = x.proy_nuevo.encode("UTF-8").decode("UTF-8")
	    
	    costo = float(x['costo_proyecto'])
	    
	   
	    
	    if int(x.fuente_fin) == 1:
		fuente_f = "SITUADO CONSTITUCIONAL"
	    elif int(x.fuente_fin) == 2:
		fuente_f = "F.C.I"
	    elif int(x.fuente_fin) == 3:
		fuente_f = "INGRESOS PROPÍOS"
	    elif int(x.fuente_fin) == 4:
		fuente_f = "OTROS"

	    
	    
	    
	    indi = x.indicador.encode("UTF-8").decode("UTF-8")
	    form = x.formula.encode("UTF-8").decode("UTF-8")
	    verificacion = x.m_verificacion.encode("UTF-8").decode("UTF-8")
	    espe = x.especifique.encode("UTF-8").decode("UTF-8")

	    if int(x.ambito) == 1:
		amb = "Internacional"
	    elif int(x.ambito) == 2:
		amb = "Nacional"
	    elif int(x.ambito) == 3:
		amb = "Estadal"
	    elif int(x.ambito) == 4:
		amb = "Municipal"
	    elif int(x.ambito) == 5:
		amb = "Parroquia"
	    elif int(x.ambito) == 6:
		amb = "Sin Extensión Territorial"

	    plan = x.plan_patria.plan_patria.encode("UTF-8").decode("UTF-8")
	    obj_h = x.obj_historico.objetivo_historico.encode("UTF-8").decode("UTF-8")
	    obj_n = x.obj_nacional.objetivo_nacional.encode("UTF-8").decode("UTF-8")
	    obj_e = x.obj_estrategico.objetivo_estrategico.encode("UTF-8").decode("UTF-8")

	    if x.obj_general_plan.objetivo_general is None:
		obj_g == ""
	    else:
		obj_g = x.obj_general_plan.objetivo_general.encode("UTF-8").decode("UTF-8")

	    
	    plan_g = x.plan_gobierno.plan_gobierno.encode("UTF-8").decode("UTF-8")
	    linea_est = x.linea_estrategica.lineas_estrategicas.encode("UTF-8").decode("UTF-8")
	    area_inv = x.area_inversion.encode("UTF-8").decode("UTF-8")

	    if int(x.tipo) == 1:
		tipo = "INVERSIÓN PRODUCTIVA"
	    elif int(x.tipo) == 2:
		tipo = "FORTALECIMEINTO INSTITUCIONAL"
	    elif int(x.tipo) == 3:
		tipo = "INFRAESTRUCTURA"
	    elif int(x.tipo) == 4:
		tipo = "SERVICIOS"

	    sector = x.sector.sectores.encode("UTF-8").decode("UTF-8")
	    problema = x.desc_problema.encode("UTF-8").decode("UTF-8")
	    obj_g_pro = x.obj_general.encode("UTF-8").decode("UTF-8")
	    impacto = x.imp_impacto.encode("UTF-8").decode("UTF-8")
	    
	    ####################################################
	    if int(x.bene_femenino) == False:
		bene_f == 0
	    else:
		bene_f = int(x.bene_femenino)
	    
	    if int(x.bene_masculino) == False:
		bene_m == 0
	    else:
		bene_m = int(x.bene_masculino)
	    
	    bene_t = int(x.bene_total)


	    ###################################################
	    if int(x.reque_accion) == 1:
		r_accion = "SI"
	    else:
		r_accion = "NO"
	    if int(x.contri_accion) == 1:
		c_accion = "SI"
	    else:
		c_accion = "NO"
	    if int(x.conflicto) == 1:
		conflic = "SI"
	    else:
		conflic = "NO"
	    ###################################################
	    if x.institucion_req.nombre_ente is None:
		int_r == ""
	    else:
		int_r = x.institucion_req.nombre_ente.encode("UTF-8").decode("UTF-8")
	    
	    if x.contri_institucion.nombre_ente is None:
		int_c == ""
	    else:
		int_c = x.contri_institucion.nombre_ente.encode("UTF-8").decode("UTF-8")
	   
	    if x.institucion_conf.nombre_ente is None:
		conf_int == ""
	    else:
		conf_int = x.institucion_conf.nombre_ente.encode("UTF-8").decode("UTF-8")
	    
	    ###################################################
	    
	    if x.explique_req == False:
		exp_r == ""
	    else:
		exp_r = x.explique_req.encode("UTF-8").decode("UTF-8")
	    if x.contri_explique == False:
		exp_c == ""
	    else:
		exp_c = x.contri_explique.encode("UTF-8").decode("UTF-8")
	    
	    if x.explique_con_conf == False:
		conf_exp == ""
	    else:
		conf_exp = x.explique_con_conf.encode("UTF-8").decode("UTF-8")
	    
	    ####################################################
	    if int(x.empleos_directos_f) == False:
		emp_dir_f == 0
	    else:
		emp_dir_f = int(x.empleos_directos_f)
	    
	    if int(x.empleos_directos_m) == False:
		emp_dir_m == 0
	    else:
		emp_dir_m = int(x.empleos_directos_m)
 
	    emp_dir_t = int(x.t_emple_directos)
	    emp_dir_i = int(x.empleados_indirectos)

	    pdf.set_y(43)
	    pdf.set_x(10)
	    #Encabezado principal
	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"1. IDENTIFICACIÓN DEL PROPONENTE".decode("UTF-8"),'LTBR',1,'C',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)
	    pdf.set_font('Arial','B',9)
	    #1. Identificación de proponente
	    pdf.cell(47,5,"1.1 Organismo/Ente/Empresa:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(143,5,ente,'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(41,5,"1.2. Fecha de Elaboración:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(17,5,fec,'TBR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(28,5,"1.4. Responsable:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(62,5,resp,'TBR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(22,5,"1.6. Teléfono:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(20,5,tel,'BTR',1,'L',1)
    
	    pdf.set_font('Arial','B',9)
	    pdf.cell(190,5,"1.3. Domicilio:".decode("UTF-8"),'LTR',1,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.multi_cell(190,5,domici,'LBR','J',1)
	    
	   
	    pdf.set_font('Arial','B',9)
	    pdf.cell(18,5,"1.5. Cargo:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(60,5,cargo,'BTR',0,'L',1)
	    
	    pdf.set_font('Arial','B',9)
	    pdf.cell(38,5,"1.7. Correo Electrónico:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(74,5,correo,'TBR',1,'L',1)
	    
	    #2.Datos del Proyecto
	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"2. DATOS DEL PROYECTO".decode("UTF-8"),'LTBR',1,'C',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(190,5,"2.1. Nombre del Proyecto:".decode("UTF-8"),'LTR',1,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.multi_cell(190,5,proyecto,'LBR',0,'J',0)

	    pdf.set_font('Arial','B',9)
	    pdf.cell(190,5,"2.2. Ubicación:".decode("UTF-8"),'LTR',1,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.multi_cell(190,5,domici,'LBR','J',1)
	    
	    pdf.set_font('Arial','B',9)
	    pdf.cell(22,5,"2.3. Duración:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(10,5,dura,'BTR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(50,5,"Fecha de Inicio y Culmincación:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(42,5,inicio,'BTR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(18,5,"Año Fiscal:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(10,5,str(fin),'TBR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(17,5,"2.4. Etapa:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(21,5,str(etapa).decode("UTF-8"),'TBR',1,'L',1)
	    

	    pdf.set_font('Arial','B',9)
	    pdf.cell(38,5,"2.5. Costo del Proyecto:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(50,5,str(costo)+" "+"Bs.",'BTR',0,'L',1)
	    
	    pdf.set_font('Arial','B',9)
	    pdf.cell(48,5,"2.6. Fuente de Financiamiento:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(54,5,str(fuente_f).decode("UTF-8"),'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(35, 5,"2.7. Indicador General: ".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(155,5,indi,'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(54,5,"2.8. Fórmula del Indicador General:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(136,5,form,'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(41, 5,"2.9. Medio de Verificación:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(149,5,verificacion,'BTR',1,'L',1)

	    
	    #3.LOCALIZACIÓN POLÍTICO ADMINISTRATIVA
	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"3. LOCALIZACIÓN POLÍTICO ADMINISTRATIVA".decode("UTF-8"),'LTBR',1,'C',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(20,5,"3.1. Ámbito:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(170,5,str(amb).decode("UTF-8"),'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(190, 5,"3.2. Específique:".decode("UTF-8"),'LTR',1,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.multi_cell(190,5,espe,'LBR','J',1)
	    #pdf.cell(108,5,espe,'BTR',1,'L',1)
	    
	    #4.ÁREA ESTRATÉGICA
	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"4. ÁREA ESTRATÉGICA".decode("UTF-8"),'LTBR',1,'C',1)
	    #4.1
	    pdf.cell(190,5,"4.1. "+plan,'LTBR',1,'L',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(190,5,"4.1.1. Objetivo Histórico:".decode("UTF-8"),'LTR',1,'L',0)
	    pdf.set_font('Arial','',8)
	    pdf.multi_cell(190,5,obj_h,1,'J',0)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(190,5,"4.1.2. Objetivo Nacional:".decode("UTF-8"),'LTR',1,'L',0)
	    pdf.set_font('Arial','',8)
	    pdf.multi_cell(190,5,obj_n,1,'J',0)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(190,5,"4.1.3. Objetivo Estratégico:".decode("UTF-8"),'LTR',1,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.multi_cell(190,5,obj_e,1,'J',0)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(190,5,"4.1.4. Objetivo General:".decode("UTF-8"),'LTR',1,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.multi_cell(190,5,obj_g,1,'J',0)
	    
	    
	    #4.2
	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"4.2. "+plan_g,'LTBR',1,'L',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)

	    pdf.set_font('Arial','B',9)
	    pdf.cell(75,5,"4.2.1. Lineas Estratégicas del Plan de Gobierno:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(115,5,linea_est,'TBR',1,'J',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(38,5,"4.2.2. Área de Inversión:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(152,5,area_inv,'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(21, 5,"4.2.3. Sector:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(169,5,sector,'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(18,5,"4.2.4. Tipo:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(172,5,str(tipo).decode("UTF-8"),'TBR',1,'J',1)
	    
	    
	    pdf.alias_nb_pages() # LLAMADA DE PAGINACION
	    pdf.add_page() # AÑADE UNA NUEVA PAGINACION
	    #5.
	    pdf.set_y(43)
	    pdf.set_x(10)
	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"5. IDENTIFICACIÓN DEL PROBLEMA Y JUSTIFICACIÓN".decode("UTF-8"),'LTBR',1,'L',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(190,5,"5.1 Descripción del problema:".decode("UTF-8"),'LTR',1,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.multi_cell(190,5,problema,'LBR','J',0)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(190,5,"5.2. Objetivo General ".decode("UTF-8"),'LTR',1,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.multi_cell(190,5,obj_g_pro,'LBR','J',0)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(190,5,"5.1. Importancia e Impacto".decode("UTF-8"),'LTR',1,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.multi_cell(190,5,impacto,'LBR','J',0)


	    #6.
	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"6. POBLACIÓN BENEFICIADA POR LA EJECUCIÓN DEL PROYECTO".decode("UTF-8"),'LTBR',1,'C',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)
	    
	    pdf.set_font('Arial','B',9)
	    pdf.cell(47,5,"6.1. Beneficiarios Femeninos:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(19,5,str(bene_f),'BTR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(47,5,"6.2. Beneficiarios Masculinos:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(19,5,str(bene_m),'BTR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(38,5,"6.3. Total Beneficiarios:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(20,5,str(bene_t),'TBR',1,'L',1)
	    
	    #7
	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"7. CONEXIONES INTER-INSTITUCIONALES".decode("UTF-8"),'LTBR',1,'C',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)

	    pdf.set_font('Arial','B',9)
	    pdf.cell(90,5,"7.1. Requiere acciones (no financieras) de otra Institución:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(100,5,r_accion,'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(28,5,"7.1.1. Institución:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(162,5,int_r,'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(25,5,"7.1.2. Explique:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(165,5,exp_r,'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(100,5,"7.2. Contribuye o complementa acciones de otras instituciones:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(90,5,c_accion,'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(28,5,"7.2.1. Institución:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(162,5,int_c,'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(25,5,"7.2.2. Explique:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(165,5,exp_c,'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(65,5,"7.3. Entra en conflicto con otra Institución:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(125,5,conflic,'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(28,5,"7.3.1. Institución:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(162,5,conf_int,'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(25,5,"7.3.2. Explique:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(165,5,conf_exp,'BTR',1,'L',1)

	    #8.

	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"8. EMPLEADOS ESTIMADOS POR LA EJECUCIÓN DEL PROYECTO".decode("UTF-8"),'LTBR',1,'C',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)
	    
	    pdf.set_font('Arial','B',9)
	    pdf.cell(75,5,"8.1. N° Estimado de empleos directos femeninos:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(20,5,str(emp_dir_f),'BTR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(77, 5,"8.2. N° Estimado de empleos directos masculinos:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(18,5,str(emp_dir_m),'BTR',1,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(70,5,"8.3. N° Estimado totales de empleos directos:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(25,5,str(emp_dir_t),'BTR',0,'L',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(60, 5,"8.2. N° Estimado de empleos directos:".decode("UTF-8"),'LTB',0,'L',1)
	    pdf.set_font('Arial','',8)
	    pdf.cell(35,5,str(emp_dir_i),'BTR',1,'L',1)

	    pdf.alias_nb_pages() # LLAMADA DE PAGINACION
	    pdf.add_page() # AÑADE UNA NUEVA PAGINAC
	    #9.
	    pdf.set_y(43)
	    pdf.set_x(10)
	    pdf.set_fill_color(199,15,15)
	    pdf.set_text_color(255,255,255)
	    pdf.set_font('Arial','B',10)
	    pdf.cell(190,5,"9. ACCIONES ESPECÍFICAS".decode("UTF-8"),'LTBR',1,'C',1)
	    pdf.set_fill_color(255,255,255)
	    pdf.set_text_color(24,29,31)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(75,4,"Nombre de la Acción Específica".decode("UTF-8"),'LTR',0,'C',1)
	    pdf.cell(30,4,"Unidad de Medida".decode("UTF-8"),'LTR',0,'C',1)
	    pdf.cell(30,4,"Medio de".decode("UTF-8"),'LTR',0,'C',1)
	    pdf.cell(40,4,"Distribución Trimestral".decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.cell(15,4,"Total".decode("UTF-8"),'LTR',1,'C',1)
	    
	    pdf.set_font('Arial','',9)
	    pdf.cell(75,4,"",'LBR',0,'C',1)
	    pdf.cell(30,4,"",'LBR',0,'C',1)
	    pdf.set_font('Arial','B',9)
	    pdf.cell(30,4,"Verificación".decode("UTF-8"),'LBR',0,'C',1)
	    pdf.set_font('Arial','',9)
	    pdf.cell(10,4,"I",'LTBR',0,'C',1)
	    pdf.cell(10,4,"II",'LTBR',0,'C',1)
	    pdf.cell(10,4,"III",'LTBR',0,'C',1)
	    pdf.cell(10,4,"IV",'LTBR',0,'C',1)
	    pdf.cell(15,4,"".decode("UTF-8"),'LBR',1,'C',1)
	   
	
	data_ids = self.read(cr, uid, ids, context=context)[0]
	payslip_id = data_ids['acciones_especificas'] # Grupo de IDS

	alm = self.pool.get('acciones.especificas') # Objeto 
	datos = alm.search(cr, uid, [('id','=',payslip_id)], context=None)
	acciones = alm.read(cr,uid,datos,context=context)


	j = 0
	for i in acciones:
	    if not int(i['trim_i']):
		i['trim_i'] = 0
	    else:
		i['trim_i']
	    if not int(i['trim_ii']):
		i['trim_ii'] = 0
	    else:
		i['trim_ii']
	    if not int(i['trim_iii']):
		i['trim_iii'] = 0
	    else:
		i['trim_iii']
	    if not int(i['trim_iv']):
		i['trim_iv'] = 0
	    else:
		i['trim_iv']
	    if not int(i['total']):
		i['total'] = 0
	    else:
		i['total']

	    n_acc = i['nombre_accion']
	    unid = i['unidad_medida']
	    med = i['medio']
	    uno = int(i['trim_i'])
	    dos = int(i['trim_ii'])
	    tres = int(i['trim_iii'])
	    cuatro = int(i['trim_iv'])

	    total_a = int(i['total'])
	    
	    
	    pdf.set_font('Arial','',7)
	    pdf.cell(75,4,n_acc.encode("UTF-8").decode("UTF-8"),'LTBR',0,'L',1)
	    pdf.cell(30,4,unid.encode("UTF-8").decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.cell(30,4,med.encode("UTF-8").decode("UTF-8"),'LTBR',0,'C',1)
	    pdf.cell(10,4,str(uno),'LTBR',0,'C',1)
	    pdf.cell(10,4,str(dos),'LTBR',0,'C',1)
	    pdf.cell(10,4,str(tres),'LTBR',0,'C',1)
	    pdf.cell(10,4,str(cuatro),'LTBR',0,'C',1)
	    pdf.cell(15,4,str(total_a),'LTBR',1,'C',1)
	    
	t_acciones = int(x['total_acciones'])
	pdf.set_font('Arial','B',9)
	pdf.cell(135,4,"Totales".encode("UTF-8").decode("UTF-8"),'LTBR',0,'C',1)
	pdf.cell(10,4,"",'LTBR',0,'C',1)
	pdf.cell(10,4,"",'LTBR',0,'C',1)
	pdf.cell(10,4,"",'LTBR',0,'C',1)
	pdf.cell(10,4,"",'LTBR',0,'C',1)
	pdf.cell(15,4,str(t_acciones),'LTBR',1,'C',1)
	
	
	pdf.set_fill_color(199,15,15)
	pdf.set_text_color(255,255,255)
	pdf.set_font('Arial','B',10)
	pdf.cell(190,5,"10. METAS FINANCIERAS".decode("UTF-8"),'LTBR',1,'C',1)
	pdf.set_fill_color(255,255,255)
	pdf.set_text_color(24,29,31)
	
	pdf.cell(98,4,"Nombre de la Acción Específica".decode("UTF-8"),'LTR',0,'C',1)
	pdf.cell(72,4,"Distribución Trimestral".decode("UTF-8"),'LTR',0,'C',1)
	pdf.cell(20,4,"Total".decode("UTF-8"),'LTR',1,'C',1)
	pdf.set_font('Arial','',9)
	pdf.cell(98,4,"".decode("UTF-8"),'LBR',0,'C',1)
	pdf.cell(18,4,"I".decode("UTF-8"),'LTBR',0,'C',1)
	pdf.cell(18,4,"II".decode("UTF-8"),'LTBR',0,'C',1)
	pdf.cell(18,4,"III".decode("UTF-8"),'LTBR',0,'C',1)
	pdf.cell(18,4,"IV".decode("UTF-8"),'LTBR',0,'C',1)
	pdf.set_font('Arial','B',9)
	pdf.cell(20,4,"".decode("UTF-8"),'LBR',1,'C',1)
    
	metas_ids = self.read(cr, uid, ids, context=context)[0]
	mts_id = metas_ids['metas_financieras'] # Grupo de IDS

	meta_fin = self.pool.get('metas.financieras') # Objeto 
	infor = meta_fin.search(cr, uid, [('id','=',mts_id)], context=None)
	metas_finan = meta_fin.read(cr,uid,infor,context=context)


	j = 0
	for l in metas_finan:
	    n_acc = l['nom_accion_metas']
	    uno = float(l['trim_1'])
	    dos = float(l['trim_2'])
	    tres = float(l['trim_3'])
	    cuatro = float(l['trim_4'])
	    total_m = float(l['total_meta'])

	    
	    
	    pdf.set_font('Arial','',8)
	    pdf.cell(98,4,n_acc.encode("UTF-8").decode("UTF-8"),'LTBR',0,'L',1)
	    pdf.cell(18,4,str(uno),'LTBR',0,'R',1)
	    pdf.cell(18,4,str(dos),'LTBR',0,'R',1)
	    pdf.cell(18,4,str(tres),'LTBR',0,'R',1)
	    pdf.cell(18,4,str(cuatro),'LTBR',0,'R',1)
	    pdf.cell(20,4,str(total_m),'LTBR',1,'R',1)

	t_metas = float(x['total_metas'])	
	pdf.set_font('Arial','B',9)
	pdf.cell(98,4,"Totales",'LTBR',0,'C',1)
	pdf.cell(18,4,"",'LTBR',0,'R',1)
	pdf.cell(18,4,"",'LTBR',0,'R',1)
	pdf.cell(18,4,"",'LTBR',0,'R',1)
	pdf.cell(18,4,"",'LTBR',0,'R',1)
	pdf.cell(20,4,str(t_metas),'LTBR',1,'R',1)
	
	 
	#pdf.alias_nb_pages() # LLAMADA DE PAGINACION
	#pdf.add_page() # AÑADE UNA NUEVA PAGINACIO
    
	#11
	#pdf.set_y(43)
	#pdf.set_x(10)
	pdf.set_fill_color(199,15,15)
	pdf.set_text_color(255,255,255)
	pdf.set_font('Arial','B',10)
	pdf.cell(190,5,"11. IMPUTACIÓN PRESUPUESTARIA".decode("UTF-8"),'LTBR',1,'C',1)
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
	imp_id = impu_ids['imputacion_presu'] # Grupo de IDS

	imp_pre = self.pool.get('imputacion.presupuestaria') # Objeto 
	imputa = imp_pre.search(cr, uid, [('id','=',imp_id)], context=None)
	imputa_presu = imp_pre.read(cr,uid,imputa,context=context)
	    

	for d in imputa_presu:
	    codi = d['codigo']
	    #partida = x.partida_presu.nombre_ente.encode("UTF-8").decode("UTF-8")
	    partida = d['partida_presu'][1]
	    tri_uno = float(d['trim_1'])
	    tri_dos = float(d['trim_2'])
	    tri_tres = float(d['trim_3'])
	    tri_cuatro = float(d['trim_4'])
	    tri_total_i = float(d['total_impu'])


	    
	    pdf.set_font('Arial','',8)
	    pdf.cell(20,4,str(codi),'LTBR',0,'L',1)
	    pdf.cell(82,4,partida.encode("UTF-8").decode("UTF-8"),'LTBR',0,'L',1)
	    pdf.cell(17,4,str(tri_uno),'LTBR',0,'R',1)
	    pdf.cell(17,4,str(tri_dos),'LTBR',0,'R',1)
	    pdf.cell(17,4,str(tri_tres),'LTBR',0,'R',1)
	    pdf.cell(17,4,str(tri_cuatro),'LTBR',0,'R',1)
	    pdf.cell(20,4,str(tri_total_i),'LTBR',1,'R',1)
	
	t_imput = float(x['total_imputaciones'])
	pdf.set_font('Arial','B',9)
	pdf.cell(102,4,"Totales",'LTBR',0,'C',1)
	pdf.cell(17,4,"",'LTBR',0,'R',1)
	pdf.cell(17,4,"",'LTBR',0,'R',1)
	pdf.cell(17,4,"",'LTBR',0,'R',1)
	pdf.cell(17,4,"",'LTBR',0,'R',1)
	pdf.cell(20,4,str(t_imput),'LTBR',1,'R',1)   
	    
	#nom = str(proyecto)+"-"+str(fec)+'.pdf'
	nom = proyecto+".pdf"



	pdf.output('/home/administrador/openerp70/modules/planificacion_presupuesto/reportes/'+nom,'F')
	
	archivo = open('/home/administrador/openerp70/modules/planificacion_presupuesto/reportes/'+nom)
	
	r_archivo = self.pool.get('reportes.presupuesto').create(cr, uid, {
		'name' : nom,
		'res_name' : nom,
		'datas' : base64.encodestring(archivo.read()),
		'datas_fname' : nom,
		'res_model' : 'proyecto.conaplan',
		'registro': "Proyectos",
		},context=context)
	
	return r_archivo
	
	  
    """
    Metodo con el cual genero el archivo .pdf 
    """

    def resumen_proyecto(self, cr, uid, ids, context=None): # Generacion de inventario

	# Instancia de la clase heredada L es horizontal y P es vertical
	# format A4, A3 o letter que son los formatos de la hoja (oficio, carta, etc)

	pdf=class_pdf.PDF3(orientation='P',unit='mm',format='letter') #HORIENTACION DE LA PAGINA
	
	#pdf.set_title(title)
	pdf.set_author('Marcel Arcuri')
	pdf.alias_nb_pages() # LLAMADA DE PAGINACION
	pdf.add_page() # AÑADE UNA NUEVA PAGINACION
	#pdf.set_font('Times','',10) # TAMANO Y TIPO DE LETRA DE LA FUENTE
	pdf.set_font('Arial','B',15)
	pdf.set_fill_color(157,188,201) # COLOR DE BORDE DE LA CELDA
	pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
	pdf.set_margins(20,5,10) # MARGENE DEL DOCUMENTO
	pdf.set_line_width(0.25)
	pdf.set_y(58)
	pdf.set_x(20)
	pdf.line(20, 73, 20, 260)
	pdf.line(20, 260, 205, 260)
	pdf.line(205, 260, 205, 73 )
	pdf.set_fill_color(255,255,255)
	pdf.set_text_color(24,29,31)
	
	resumen = self.browse(cr, uid, ids, context=context)
	npro = ""
	obj_g = ""

	for x in resumen:
	    ente = x.organismo.nombre_ente.encode("UTF-8").decode("UTF-8")
	    fec = x.f_solicitud.split("/")
	    fec_ley = fec[2]
	    proyecto = x.nombre_pro.encode("UTF-8").decode("UTF-8")
	    obj_g_pro = x.obj_general.encode("UTF-8").decode("UTF-8")
	    costo = float(x['costo_proyecto'])
	    
	    obj_h = x.obj_historico.objetivo_historico.encode("UTF-8").decode("UTF-8")
	    obj_n = x.obj_nacional.objetivo_nacional.encode("UTF-8").decode("UTF-8")
	    obj_e = x.obj_estrategico.objetivo_estrategico.encode("UTF-8").decode("UTF-8")

	    if x.obj_general_plan.objetivo_general is None:
		obj_g == ""
	    else:
		obj_g = x.obj_general_plan.objetivo_general.encode("UTF-8").decode("UTF-8")

	    
	    plan_g = x.plan_gobierno.plan_gobierno.encode("UTF-8").decode("UTF-8")
	    linea_est = x.linea_estrategica.lineas_estrategicas.encode("UTF-8").decode("UTF-8")
	    
	    hist = "OBJETIVO HISTÓRICO: ".decode("UTF-8")
	    estr = "OBJETIVO ESTRATÉGICO: ".decode("UTF-8")
	    linea = "LÍNEA ESTRÁTEGICA DEL PAN DE GOBIERNO: ".decode("UTF-8")
	    pdf.set_y(5)
	    pdf.set_x(97)
	    pdf.set_font('Times','',4)
	    pdf.write(20,"REPÚBLICA BOLIVARIANA".decode("UTF-8"))
	    pdf.set_y(7)
	    pdf.set_x(101)
	    pdf.write(20,"DE VENEZUELA".decode("UTF-8"))
	    
	    pdf.set_y(36)
	    pdf.set_x(98)
	    pdf.write(20,"CONSEJO LEGISLATIVO".decode("UTF-8"))
	    pdf.set_y(38)
	    pdf.set_x(99)
	    pdf.write(20,"DEL ESTADO ARAGUA".decode("UTF-8"))
	    
	    pdf.set_font('Times','',7)
	    pdf.set_y(50)
	    pdf.set_x(20)
	    pdf.cell(150,4,ente.upper(),'LTB',0,'L',1)
	    pdf.cell(35,4,"LEY DE PRESUPUESTO "+str(fec_ley).decode("UTF-8"),'TBR',1,'L',1)
	    pdf.multi_cell(185,4,"PROYECTO: "+proyecto.upper(),'LTR','J',1)
	    pdf.multi_cell(185,4,"OBJETIVO GENERAL DEL PROYECTO: "+obj_g_pro.upper(),'LR','J',1)
	    pdf.cell(185,4,"MONTO: "+str(costo)+" Bolívares",'LR',1,'J',1)
	    pdf.multi_cell(185,4,hist+obj_h.upper(),'LR','J',1)
	    pdf.multi_cell(185,4,"OBJETIVO NACIONAL: "+obj_n.upper(),'LR','J',1)
	    pdf.multi_cell(185,4,estr+obj_e.upper(),'LR','J',1)
	    pdf.multi_cell(185,4,"OBJETIVO GENERAL: "+obj_g.upper(),'LR','J',1)
	    pdf.multi_cell(185,4,linea+linea_est.upper(),'LR','L',1)
	    
	    
	    pdf.cell(25,4,"ESTRUCTURA".decode("UTF-8"),'LTR',0,'C',1)
	    pdf.cell(55,4,"".decode("UTF-8"),'LT',0,'C',1)
	    pdf.cell(105,4,"FUENTE DE FINANCIAMIENTO".decode("UTF-8"),'LTBR',1,'C',1)
	    
	    pdf.cell(25,3,"PRESUPUESTARIA ".decode("UTF-8"),'LR',0,'C',1)
	    pdf.cell(55,3,"DENOMINACIÓN".decode("UTF-8"),'LR',0,'C',1)
	    pdf.cell(25,3,"SITUADO".decode("UTF-8"),'LTR',0,'C',1)
	    pdf.cell(20,3,"GESTIÓN".decode("UTF-8"),'LTR',0,'C',1)
	    pdf.cell(30,3,"FONDO COMPENSACIÓN".decode("UTF-8"),'LTR',0,'C',1)
	    pdf.cell(30,3,"TOTAL".decode("UTF-8"),'LTR',1,'C',1)
	    pdf.cell(25,3," ".decode("UTF-8"),'LBR',0,'C',1)
	    pdf.cell(55,3,"".decode("UTF-8"),'LBR',0,'C',1)
	    pdf.cell(25,3,"CONSTITUCIONAL".decode("UTF-8"),'LBR',0,'C',1)
	    pdf.cell(20,3,"FISCAL".decode("UTF-8"),'LBR',0,'C',1)
	    pdf.cell(30,3,"INTERTERRITORIAL".decode("UTF-8"),'LBR',0,'C',1)
	    pdf.cell(30,3,"PRESUPUESTO 2014".decode("UTF-8"),'LBR',1,'C',1)
	    pdf.cell(185,4,"".decode("UTF-8"),'LTR',1,'C',1)
	    impu_ids = self.read(cr, uid, ids, context=context)[0]
	    imp_id = impu_ids['imputacion_presu'] # Grupo de IDS

	    imp_pre = self.pool.get('imputacion.presupuestaria') # Objeto 
	    imputa = imp_pre.search(cr, uid, [('id','=',imp_id)], context=None)
	    imputa_presu = imp_pre.read(cr,uid,imputa,context=context)

    
	    for d in imputa_presu:
		codi = d['codigo']
		#partida = x.partida_presu.nombre_ente.encode("UTF-8").decode("UTF-8")
		partida = d['partida_presu'][1]
		tri_total_i = float(d['total_impu'])

		pdf.cell(25,6,str(codi),'L',0,'C',1)
		pdf.cell(55,6,partida.encode("UTF-8").decode("UTF-8"),'',0,'L',1)
		pdf.cell(25,6,str(tri_total_i),'',0,'R',1)
		pdf.cell(20,6,"0,00".decode("UTF-8"),'',0,'R',1)
		pdf.cell(30,6,"0,00".decode("UTF-8"),'',0,'R',1)
		pdf.cell(30,6,str(tri_total_i),'R',1,'R',1)
 
	    total_pro = float(x['total_imputaciones'])
	    pdf.set_y(255)
	    pdf.set_x(20)
	    pdf.cell(155,5,"TOTAL",'LTBR',0,'L',1)
	    #pdf.set_y(200)
	    #pdf.set_x(175)
	    pdf.cell(30,5,str(total_pro),'LTBR',0,'R',1)
	    
	    nom = "Resumen"+".pdf"

	    pdf.output('openerp/addons/planificacion_presupuesto/reportes/'+nom,'F')
	    
	    
	  #Funciones para la validación de las fechas de inicio y fin de un proyecto
    def duracion_proyecto(self, cr, uid, ids, fecha_ini, fecha_fin, context=None): 

	retorno = {}
	res = {}
	values = {}
	valores = {}
	dias_mes_anterior = 0
	now = datetime.now().strftime('%Y-%m-%d')
	
	#Vaildar si la fecha final es anterior a la actual
	val_fecha_fin = self.onchange_fh_final(cr, uid, ids, fecha_fin, context=context)
	print val_fecha_fin
	
	#Vaildar si la fecha inicial es anterior a la actual
	val_fecha_ini = self.onchange_fh_inicio(cr, uid, ids, fecha_ini, context=context)
	print val_fecha_ini
	
	if fecha_ini and fecha_fin:
	    fecha_inicial = fecha_ini.split("-")

	    anyo_ini = fecha_inicial[0]
	    mes_ini = fecha_inicial[1]
	    dia_ini = fecha_inicial[2]
	    

	    fecha_final = fecha_fin.split("-")
	    
	    anyo_final = fecha_final[0]
	    mes_final = fecha_final[1]
	    dia_final = fecha_final[2]

	    dia_diferencia = int(dia_final) - int(dia_ini)
	    mes_diferencia = int(mes_final) - int(mes_ini)
	    anyo_diferencia = int(anyo_final) - int(anyo_ini)

	    # se suma dia_diferencia los dias que tiene el mes anterior de la fecha final

	    if dia_diferencia < 0:
		mes_diferencia = int(mes_diferencia)-1

		if mes_final:

		    if mes_final == 1 or mes_final == 3 or mes_final == 5 or mes_final == 7 or mes_final == 8 or mes_final == 10 or mes_final == 12:
			dias_mes_anterior = 31

		    elif mes_final == 2: # calculo si un año es bisiesto

			if ((((anyo_final%100)!=0) and ((anyo_final%4)==0)) or ((anyo_final%400)==0)):
			    #print 'El año es Bisiesto'
			    dias_mes_anterior = 29
			else:
			    #print 'El año no es Bisiesto'
			    dias_mes_anterior = 28

		    elif mes_final == 4 or mes_final == 6 or mes_final == 9 or mes_final == 11:
			dias_mes_anterior = 30	

		dia_diferencia = int(dia_diferencia) + int(dias_mes_anterior)

	    if mes_diferencia < 0:
		anyo_diferencia = int(anyo_diferencia) - 1  
		mes_diferencia = int(mes_diferencia) + 12

	    # Se valida si cumple un año se muestre año si es mayor de un año se muestre años
	    if anyo_diferencia < 2:
		anyo_diferencia = str(anyo_diferencia)+" Año"
	    elif anyo_diferencia > 1:
		anyo_diferencia = str(anyo_diferencia)+" Años"

	    if mes_diferencia < 2:
		mes_diferencia = str(mes_diferencia)+" Mes"
	    elif mes_diferencia > 1:
		mes_diferencia = str(mes_diferencia)+" Meses"

	    if dia_diferencia < 2:
		dia_diferencia = str(dia_diferencia)+" Dia"
	    elif dia_diferencia > 1:
		dia_diferencia = str(dia_diferencia)+" Dias"


	    #~ duracion_proyec = str(anyo_diferencia).replace('-',"")+" "+str(mes_diferencia)+" "+str(dia_diferencia)
	    duracion_proyec = str(anyo_diferencia).replace('-',"")+" "+str(mes_diferencia)
	    
	    #~ self.write(cr, uid, ids, {'ano_antiguedad':str(anyo_diferencia).replace('-',"")}, context=context)
	    
	    values.update({'duracion' : duracion_proyec,})
		
	else:
	    values = "vacio"
	
	valores = {'value' : values}
	
	retorno = valores

	return retorno
				
    def onchange_fh_inicio(self, cr, uid, ids, fh_inicio, context):
	res = {}
	now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	if fh_inicio < now:
		res['warning'] = {'title': "Cuidado: Error!",'message' : "No puede seleccionar como fecha de inicio dias pasados",}
		return res
	return res
				    
    def onchange_fh_final(self, cr, uid, ids, fh_final, context):
	res = {}
	now = datetime.now().strftime('%Y-%m-%d')
	if fh_final < now:
		res['warning'] = {'title': "Atencion: Error!",'message' : "No puede seleccionar como fecha final dias anteriores a hoy",}
		return res
	return res
				  

    _columns = {
	'estatus': fields.selection([('1','Revisando'), ('2','Rechazado'), ('3','Para Ajuste'), ('4','Aprobado')], string="Estatus"),
        'c_solicitud' : fields.char(string="ID", size=255, required=False, readonly=True),
	'user_register': fields.many2one('res.users', 'Registrado por:', readonly=True),
	#'archivos': fields.function(_data_get, fnct_inv=_data_set, string='Cargar Archivos', type="binary", nodrop=True),
	'archivos': fields.binary('Adjuntar Archivo'),
	
	#Pestaña1
	'organismo': fields.many2one('organos.entes', 'Organismo/Ente/empresa:', required=True),
        'f_solicitud': fields.char('Fecha de Elaboración:', required=True, readonly=True),
	'domicilio': fields.char('Domicilio:', required=True),
	'responsable': fields.char('Responsable:', required=True),
	'cargo': fields.char('Cargo:', required=True),
	'telefono': fields.char('Teléfono:', required=True),
	'correo': fields.char('Correo Electrónico:', required=True),
	'siglas': fields.char('Siglas:'),
	#Pestaña2
	'nombre_pro': fields.char('Nombre del Proyecto', required=True),
	'ubicacion': fields.char('Ubicación',  required=True),
	'fecha_ini_fin' : fields.char('Fecha de Inicio y Culminación',  readonly=True,  required=True),
	'year_fiscal': fields.selection([(num, str(num)) for num in range(2013, (datetime.now().year)+30 )], 'Año Fiscal', required=True),
	'duracion': fields.char('Duración:',  readonly=True,  required=True),
	'etapa': fields.selection([('1','Nueva'), ('2','Continuación')], string="Etapa", required=True),
	'proy_nuevo': fields.char('Proyecto Nuevo', required=False),
	'costo_proyecto': fields.float('Costo del Proyecto', readonly=False),
	'fuente_fin': fields.selection([('1','SITUADO CONSTITUCIONAL'), ('2','F.C.I'), ('3','INGRESOS PROPÍOS'), ('4','OTROS')], string="Fuente de Financiamiento:", readonly=True),
	'indicador': fields.char('Indicador General', size=120, required=True),
	'formula': fields.char('Fórmula del Indicador General:', size=100, required=True),
	'm_verificacion': fields.char('Medio de Verificación:', size=120, required=True),
	#Pestaña3
	'ambito': fields.selection([('1','Internacional'), ('2','Nacional'), ('3','Estadal'),
	    ('4','Municipal'), ('5','Parroquia'),('6','Sin Extensión Territorial'),('7','Comunal')
	    ], string="Ámbito", required=True),
	'especifique': fields.text('Específique:', size=200, required=True),
	#Pestaña4
	'obj_general_plan' : fields.many2one('objetivo.general', 'Objetivos Generales', required=False),
	'obj_estrategico' : fields.many2one('objetivo.estrategico', 'Objetivos Estratégico', required=True),
	'obj_nacional' : fields.many2one('objetivo.nacional', 'Objetivos Nacional', required=True),
	'obj_historico' : fields.many2one('objetivo.historico', 'Objetivos Historicos', required=True),
	'plan_patria': fields.many2one('plan.patria', 'Plan de la Patria', required=True),
	'plan_gobierno': fields.many2one('plan.gobierno', 'Plan de Gobierno', required=True),
	'linea_estrategica': fields.many2one('lineas.estrategicas', 'Lineas estrategicas de Accion', required=True),
	'area_inversion': fields.char('Área de Inversión:', size=120, required=True),
	'tipo': fields.selection([('1','Inversion Productiva'), ('2','Fortalecimiento Institucional'),
	    ('3','Infraestructura'), ('4','Servicios')], string="Tipo de Inversión", required=True),
	'sector':fields.many2one('organos.sectores', 'Sector', ondelete='cascade', select=False, required=True),
	#Pestaña 5
	'desc_problema': fields.text('Descripción del problema:', size=1700, required=True),
	'obj_general': fields.text('Objetivo General:', size=250, required=True),
	'imp_impacto': fields.text('Importancia e Impacto:', size=300, required=True),
	#Pestaña 6
	'bene_femenino': fields.integer('Beneficiarios Femeninos:', required=False),
	'bene_masculino': fields.integer('Beneficiarios Masculinos:', required=False),
	'bene_total': fields.integer('Beneficiarios Totales:', required=True, readonly=False),
	#Pestaña 7
	'reque_accion': fields.selection([('1','SI'), ('2','NO')], string="7.1. Requiere acciones (no financieras) de otra institución:"),
	'institucion_req': fields.many2one('organos.entes', 'Institución:', required=False),
	'explique_req': fields.char('Explique:', size=120, required=False),
	'contri_accion': fields.selection([('1','SI'), ('2','NO')], string="7.2. Contribuye o complementa acciones de otras instituciones:"),
	'contri_institucion': fields.many2one('organos.entes', 'Institución:', required=False),
	'contri_explique': fields.char('Explique:', size=120, required=False),
	'conflicto': fields.selection([('1','SI'), ('2','NO')], string="7.3. Entra en conflicto con otras instituciones:"),
	'institucion_conf': fields.many2one('organos.entes', 'Institución:', required=False),
	'explique_con_conf': fields.char('Explique:', size=120, required=False),
	#pestaña8
	'empleos_directos_f': fields.integer('N° Estimado de empleaos directos femeninos:', required=False),
	'empleos_directos_m': fields.integer('N° Estimado de empleaos directos masculinos:', required=False),
	't_emple_directos': fields.integer('N° Estimado totales de empleos directos:', required=True, readonly=False),
	'empleados_indirectos': fields.integer('N° Estimado de empleos indirectos:', required=True),
	#pestañas9
	'acciones_especificas':fields.one2many('acciones.especificas', 'acciones_ids',required=False),
	'total_acciones':fields.float(string="Cant. total", required=False), #Nuevo
	#pestañas10
	'metas_financieras':fields.one2many('metas.financieras', 'metas_ids',required=False),
	'total_metas':fields.float(string="Cant. total", required=False), #Nuevo
	#pestañas11
	'imputacion_presu':fields.one2many('imputacion.presupuestaria', 'imputacion_ids',required=False),
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
	'duracion': "1 Año",
	'fecha_ini_fin': "01 de Enero / 31 de Diciembre",
        'user_register': lambda s, cr, uid, c: uid,
	'reque_accion': '2',
	'contri_accion': '2',
	'conflicto': '2',
	'estatus': '1',
    }
    
    #Método para copiar las acciones de la pestañe de 'Acciones' a la pestaña de 'Metas'
    def carga_acciones(self, cr, uid, ids, context=None):
			#Modelo a escribir
			metas = self.pool.get('metas.financieras')
			
			#Modelo actual
			browse_id = self.browse(cr, uid, ids, context=context)
			
			id_m = ""
			id_proyecto = 0
			for proyecto in browse_id:
				id_proyecto = proyecto.id
				
				accion = ""
				r = False
				i = 1
				for accion in proyecto.acciones_especificas:
					
					if accion.nombre_accion:
						#~ print "Acción "+str(i)+": "+str(accion.nombre_accion).encode('UTF-8')
						accion = accion.nombre_accion.encode('UTF-8')
						
						#Verificamos si ya existe la acción en el modelo correspondiente
						buscar_m = metas.search(cr, uid, [('metas_ids','=',id_proyecto),('nom_accion_metas','=',accion)], count=False)
						if not buscar_m:
							#Carga de las acciones en el modelo correspondiente
							id_m = metas.create(cr, uid, {
								'metas_ids' : id_proyecto,
								'nom_accion_metas' : accion,
							},context=context)
							
							if id_m:
								r = True
								
					#Aumento del contador
					i = i + 1
					
			return r
    
    #Función para el cálculo del monto total de las metas del proyecto________________________________________________________________________________
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
		for meta in proyecto.metas_financieras:
			cantidad_meta_m = meta.total_meta
			total_metas = total_metas + cantidad_meta_m
			#~ print "cant. meta"+str(i+1)+": "+str(cantidad_meta_m)
		#~ print "Total metas: "+str(total_metas)+"\n"
		i = i + 1
		
	#Segmento que obtiene los montos directamente de la vista
	j = 0
	for mt in metas:
		#~ print "Registro meta"+str(j+1)+": "+str(mt)
		#~ print "Datos meta"+str(j+1)+": "+str(mt[2])
		if not mt[2]:
			#~ print "0.0"
			cantidad_meta_v = 0
			total_metas = total_metas + cantidad_meta_v
		else:
			#~ print mt[2]['total_meta']
			cantidad_meta_v = mt[2]['total_meta']
			total_metas = total_metas + cantidad_meta_v
			
		j = j + 1
	
	values.update({
		'total_metas' : total_metas,
		'costo_proyecto' : total_metas,
	})
	
	return {'value':values}
					
				
    #~ Función para el cálculo del monto total de las imputaciones presupuestarias________________________________________________________________________________
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
		for imputacion in proyecto.imputacion_presu:
			cantidad_imp_m = imputacion.total_impu
			total_imputaciones = total_imputaciones + cantidad_imp_m
			#~ print "cant. meta"+str(i+1)+": "+str(cantidad_imp_m)
		#~ print "Total metas: "+str(total_metas)+"\n"
		i = i + 1
		
	#Segmento que obtiene los montos directamente de la vista
	j = 0
	for imp in imputaciones:
		#~ print "Registro imputación"+str(j+1)+": "+str(imp)
		#~ print "Datos imputación"+str(j+1)+": "+str(imp[2])
		if not imp[2]:
			#~ print "0.0"
			cantidad_imp_v = 0
			total_imputaciones = total_imputaciones + cantidad_imp_v
		else:
			#~ print mt[2]['total_impu']
			cantidad_imp_v = imp[2]['total_impu']
			total_imputaciones = total_imputaciones + cantidad_imp_v
			
		j = j + 1
	
	values.update({
		'total_imputaciones' : total_imputaciones,
	})
	
	return {'value':values}
				
				
    #~ Función para el cálculo de la cantidad total de acciones________________________________________________________________________________
    def total_acciones(self, cr, uid, ids, acciones, context=None):
			
	values = {}
	
	cantidad_acc_m = 0
	
	cantidad_acc_v = 0
	
	total_acciones = 0

	browse_id = self.browse(cr, uid, ids, context=context)
	
	#Segmento que obtiene los montos directamente del modelo
	i = 0
	for proyecto in browse_id:
		i = 0
		for accion in proyecto.acciones_especificas:
			cantidad_acc_m = accion.total
			total_acciones = total_acciones + cantidad_acc_m
			#~ print "cant. acción"+str(i+1)+": "+str(cantidad_acc_m)
		#~ print "Total acciones: "+str(total_acciones)+"\n"
		i = i + 1
		
	#Segmento que obtiene los montos directamente de la vista
	j = 0
	for acc in acciones:
		#~ print "Registro acción"+str(j+1)+": "+str(acc)
		#~ print "Datos acción"+str(j+1)+": "+str(acc[2])
		if not acc[2]:
			#~ print "0.0"
			cantidad_acc_v = 0
			total_acciones = total_acciones + cantidad_acc_v
		else:
			#~ print acc[2]['total']
			cantidad_acc_v = acc[2]['total']
			total_acciones = total_acciones + cantidad_acc_v
			
		j = j + 1
	
	values.update({
		'total_acciones' : total_acciones,
	})
	
	return {'value':values}

