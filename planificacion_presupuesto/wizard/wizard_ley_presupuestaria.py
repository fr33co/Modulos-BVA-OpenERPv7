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
import sys
from openerp import tools
from openerp.osv import fields,osv
from openerp import SUPERUSER_ID
from openerp.tools.translate import _
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
reload(sys)
sys.setdefaultencoding("utf-8")

class wizard_resumen(osv.osv_memory):

    _name = "wizard.ley.presupuestaria"
    
    #_order = "wizard_resumen"
    
    
    def resumen_ley_presupuestaria(self, cr, uid, ids, context=None): #Generacion de inventario
        
        
        resumen = self.browse(cr, uid, ids, context=context)
        for m in resumen:
            fecha = m.year_fiscal
                        
        pdf=class_pdf.PDF4(orientation='P',unit='mm',format='letter') #ORIENTACION DE LA PAGINA
        #pdf.set_title(title)
        pdf.set_author('Yorle Rodrìguez')
        pdf.alias_nb_pages() # LLAMADA DE PAGINACION
        #pdf.add_page() # AÑADE UNA NUEVA PAGINACION
        #pdf.set_font('Times','',10) # TAMANO DE LA FUENTE
        pdf.set_font('Arial','B',15)
        pdf.set_fill_color(255,255,255) # COLOR DEL BORDE DE LA CELDA
        pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
        #pdf.set_margins(20,5,10) # MARGEN DEL DOCUMENTO
        #pdf.ln(20) # Saldo de linea
        # 10 y 50 eje x y y 200 dimencion
        #pdf.line(10, 40, 200, 40) Linea 
        pdf.set_line_width(0.5)
         
        
        cr.execute('SELECT distinct oe.id,oe.nombre_ente from organos_entes as oe inner join accion_centralizada as ac on oe.id=ac.organismo inner join proyecto_conaplan as pc on oe.id=pc.organismo inner join observacion_accion as oa on ac.id=oa.codigo inner join observacion_proyecto as op on pc.id=op.codigo where year_fiscal = '+str(fecha)+' and ac.estatus=\'4\' or pc.estatus=\'4\'')
        for resumen in cr.fetchall():
            pdf.add_page() # AÑADE UNA NUEVA PAGINACION
            id_ente = resumen[0]
            ente    = resumen[1]

            pdf.set_text_color(24,29,31)
            pdf.set_line_width(0.25)
            pdf.set_font('Times','B',12)
            pdf.set_y(130)
            pdf.set_x(60)
           
            pdf.multi_cell(80,4,ente,0,'C',1)
            
        ##~ ############################################################################################################
        ##~ ############################################### PAGINA 1####################################################
        ##~ ############################################################################################################
            #pdf=PDF(orientation='P',unit='mm',format='letter') #ORIENTACION DE LA PAGINA
            #pdf.set_title(title)
            #pdf.set_author('Yorle Rodrìguez')
            pdf.alias_nb_pages() # LLAMADA DE PAGINACION
            pdf.add_page() # AÑADE UNA NUEVA PAGINACION
            #pdf.set_font('Times','',10) # TAMANO DE LA FUENTE
            pdf.set_font('Arial','B',15)
            pdf.set_fill_color(157,188,201) # COLOR DEL BORDE DE LA CELDA
            pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
            pdf.set_margins(20,5,10) # MARGEN DEL DOCUMENTO
            #pdf.ln(20) # Saldo de linea
            # 10 y 50 eje x y y 200 dimencion
            #pdf.line(10, 40, 200, 40) Linea 
            pdf.set_line_width(0.5)
            
            pdf.set_line_width(0.25)
            pdf.set_y(58)
            pdf.set_x(20)
            pdf.line(20, 73, 20, 258)
            #~ pdf.line(20, 260, 205, 260)
            pdf.line(205, 258, 205, 73 )
             
             
            pdf.set_fill_color(234,233,229)
            pdf.set_text_color(24,29,31)
            pdf.set_line_width(0.25)
            pdf.set_font('Times','B',7)
            pdf.set_y(50)
            pdf.set_x(20)
            pdf.ln(7)
            pdf.cell(150,4,ente,'LTBR',0,'L',1)
            pdf.cell(35,4,"LEY DE PRESUPUESTO "+str(fecha),'TR',1,'L',1)
            
            ########### Comienzo Accion Centralizada #################
            tot_acc = 0
            por_y          = 69
            i = 10
            tot_presu1     = 0.00
            cr.execute('SELECT COUNT(oa.codigo) AS cantidad FROM observacion_accion AS oa INNER JOIN accion_centralizada AS ac ON oa.codigo=ac.id WHERE ac.organismo='+str(id_ente)+' AND ac.estatus=\'4\'') 
            for aprobadas in cr.fetchall():
                tot_acc = aprobadas[0]
                
                
                if tot_acc > 0:
                    l = 1
                    cr.execute('SELECT oa.estruc_presu, oa.accion_centra, oa.fuente_fin, oa.monto FROM observacion_accion AS oa INNER JOIN accion_centralizada AS ac ON oa.codigo=ac.id WHERE oa.ente='+str(id_ente)+' AND ac.estatus=\'4\' ORDER BY ac.id')
                    
                    #if( l <= tot_acc):
                            
                    pdf.multi_cell(185,4,"RESUMEN DE LAS ACCIONES CENTRALIZADAS (EN BOLIVARES)".decode("UTF-8"),'LRTB','J',1)
                    pdf.set_font('Times','B',5)
                    pdf.set_fill_color(249,240,204)
                    
                    pdf.multi_cell(22,7,"ESTRUCTURA PRESUPUESTARIA".decode("UTF-8"),'LTBR','C',1)
                    pdf.set_y(65)
                    pdf.set_x(42)
                    pdf.cell(38,14,"DENOMINACIÓN".decode("UTF-8"),'LRBT',0,'C',1)
                    pdf.cell(125,4,"FUENTE DE FINANCIAMIENTO".decode("UTF-8"),'LTRB',1,'C',1)
                    pdf.set_y(69)
                    pdf.set_x(80)
                    pdf.multi_cell(25,5,"SITUADO CONSTITUCIONAL".decode("UTF-8"),'BLTR','C',1)
                    pdf.set_y(69)
                    pdf.set_x(102)
                    pdf.multi_cell(15,5,"GESTIÓN FISCAL".decode("UTF-8"),'LTRB','C',1)
                    pdf.set_y(69)
                    pdf.set_x(117)
                    pdf.multi_cell(28,5,"FONDO DE COMPENSACIÓN INTERTERRITORIAL".decode("UTF-8"),'LTRB','C',1)
                    pdf.set_y(69)
                    pdf.set_x(145)
                    pdf.multi_cell(35,5,"TRANSFERENCIAS CORRIENTES INTERNAS DE LA REPÚBLICA".decode("UTF-8"),'LTRB','C',1)
                    pdf.set_y(69)
                    pdf.set_x(180)
                    pdf.multi_cell(25,5,"TOTAL PRESUPUESTO "+str(fecha),'LTRB','C',1)
                     
                    pdf.set_fill_color(255,255,255)
                            
                   
                    
                   
                    montot         = 0.00
                    for acciones in cr.fetchall():
                        
                        estructura     = acciones[0]
                        monto_sc       = 0.00
                        monto_gf       = 0.00
                        monto_fci      = 0.00
                        monto_tci      = 0.00
                        accion_centra  = acciones[1]
                        fuente_fin     = acciones[2]
                        monto_no       = acciones[3]
                      
                        
                        if estructura != None:
                            #print str(estructura)
                            
                            pdf.set_font('Times','',7)
                            pdf.cell(22,4,estructura,'L',0,'L',1)
                            pdf.multi_cell(38,4,accion_centra.encode("UTF-8").decode("UTF-8"),0,'J',1)
                            pdf.set_y(por_y+i)
                            pdf.set_x(85)
                            
                            #print fuente_fin
                                                    
                            if fuente_fin == "1":
                                monto_sc=monto_no
                            if fuente_fin == "2":
                                monto_gf=monto_no
                            if fuente_fin == "3":
                                monto_fci=monto_no
                            if fuente_fin == "4":
                                monto_tci=monto_no
                            
                            tot_presu1 += monto_no
                            montot=monto_sc+monto_gf+monto_fci+monto_tci
                            pdf.cell(17,4,str(monto_sc),0,0,'R',1)
                            pdf.cell(15,4,str(monto_gf),0,0,'R',1)
                            pdf.cell(28,4,str(monto_fci),0,0,'R',1)
                            pdf.cell(35,4,str(monto_tci),0,0,'R',1)
                            pdf.cell(25,4,str(montot),'R',1,'R',1)
                            pdf.set_y(89 )
                            i = i + 10
                        
                    pdf.ln(10)
                    #pdf.set_y(10)
                    pdf.set_font('Times','B',7)
                    pdf.cell(160,4,"Sub-Total Acción Centralizada".decode("UTF-8"),'LTBR',0,'L',1)
                    pdf.cell(25,4,"Bs. "+str(tot_presu1),'LTBR',1,'R',1)
                    
                    pdf.set_y(110)
                    pdf.set_fill_color(234,233,229)
                    
            ############ Fin Accion Centralizada ########################
            
            
            ############ Comienzo de Proyecto ########################
            tot_proy = 0
            tot_presu2     = 0.00
            cr.execute('SELECT COUNT(op.codigo) AS cantidad FROM observacion_proyecto AS op INNER JOIN proyecto_conaplan AS pc ON op.codigo=pc.id WHERE pc.organismo='+str(id_ente)+' AND pc.estatus=\'4\'') 
            for aprobados in cr.fetchall():
               tot_proy = aprobados[0]
               if tot_proy > 0:
                m = 1
                cr.execute('SELECT op.estruc_presu, op.nombre_pro, op.fuente_fin, op.monto FROM observacion_proyecto AS op INNER JOIN proyecto_conaplan AS pc ON op.codigo=pc.id WHERE op.ente='+str(id_ente)+' AND pc.estatus=\'4\'')
                
               
                montot         = 0.00
                k = 0
                if tot_acc > 0 and tot_proy > 0:
                    p = 114
                    g = 118
                    w = por_y+i
                    y =128
                elif tot_acc > 0 and  tot_proy == 0:
                    p = 114
                    g = 118
                    w = por_y+i
                    y = 128
                elif tot_acc == 0 and  tot_proy > 0:
                    p = 114 - 49
                    g = 118 - 49
                    w = w = por_y+i - 49
                    y = 128 - 49
                    
                for proyectos in cr.fetchall():
                    estruc_presu     = proyectos[0]
                    monto_sc         = 0.00
                    monto_gf         = 0.00
                    monto_fci        = 0.00
                    monto_tci        = 0.00
                    nombre_pro       = proyectos[1]
                    fuente_fin       = proyectos[2]
                    monto            = proyectos[3]
                    
                    print estruc_presu 
                    if( m <= tot_proy):
                        
                        pdf.multi_cell(185,4,"RESUMEN DE PROYECTOS".decode("UTF-8"),'LTRB','J',1)
                        pdf.set_font('Times','B',5)
                        pdf.set_fill_color(249,240,204)
                        
                        pdf.multi_cell(22,7,"ESTRUCTURA PRESUPUESTARIA".decode("UTF-8"),'LTBR','C',1)
                        pdf.set_y(p)
                        pdf.set_x(42)
                        pdf.cell(38,14,"DENOMINACIÓN".decode("UTF-8"),'LRBT',0,'C',1)
                        pdf.cell(125,4,"FUENTE DE FINANCIAMIENTO".decode("UTF-8"),'LTRB',1,'C',1)
                        pdf.set_y(g)
                        pdf.set_x(80)
                        pdf.multi_cell(25,5,"SITUADO CONSTITUCIONAL".decode("UTF-8"),'LTRB','C',1)
                        pdf.set_y(g)
                        pdf.set_x(102)
                        pdf.multi_cell(15,5,"GESTIÓN FISCAL".decode("UTF-8"),'LTRB','C',1)
                        pdf.set_y(g)
                        pdf.set_x(117)
                        pdf.multi_cell(28,5,"FONDO DE COMPENSACIÓN INTERTERRITORIAL".decode("UTF-8"),'LTRB','C',1)
                        pdf.set_y(g)
                        pdf.set_x(145)
                        pdf.multi_cell(35,5,"TRANSFERENCIAS CORRIENTES INTERNAS DE LA REPÚBLICA".decode("UTF-8"),'LTRB','C',1)
                        pdf.set_y(g)
                        pdf.set_x(180)
                        pdf.multi_cell(25,10,"TOTAL PRESUPUESTO"+str(fecha),'LTRB','C',1)
                        
                        pdf.set_fill_color(255,255,255)
                            
                            
                        if estruc_presu != None:
                                #print str(estruc_presu)
                                
                                pdf.set_font('Times','',7)
                                pdf.cell(22,4,estruc_presu,'L',0,'L',1)
                                pdf.multi_cell(38,4,nombre_pro.encode("UTF-8").decode("UTF-8"),0,'J',1)
                                pdf.set_y(w)
                                pdf.set_x(85)
                                
                                #print fuente_fin
                                                        
                                if fuente_fin == "1":
                                    monto_sc=monto
                                if fuente_fin == "2":
                                    monto_gf=monto
                                if fuente_fin == "3":
                                    monto_fci=monto
                                if fuente_fin == "4":
                                    monto_tci=monto
                                
                        tot_presu2 += monto
                        montot=monto_sc+monto_gf+monto_fci+monto_tci
                        pdf.set_y(y)
                        pdf.set_x(85)
                        pdf.cell(17,4,str(monto_sc),0,0,'R',1)
                        pdf.cell(15,4,str(monto_gf),0,0,'R',1)
                        pdf.cell(28,4,str(monto_fci),0,0,'R',1)
                        pdf.cell(35,4,str(monto_tci),0,0,'R',1)
                        pdf.cell(25,4,str(montot),'R',1,'R',1)
                               
                        pdf.ln(30)
                        pdf.set_font('Times','B',7)
                        pdf.cell(160,4,"Sub-Total de Proyectos".decode("UTF-8"),'LTBR',0,'L',1)
                        pdf.cell(25,4,"Bs. "+str(tot_presu2),'LTBR',1,'R',1)
                        #k = k - 90  
            pdf.set_y(255)
            pdf.set_x(20)
            pdf.set_fill_color(255,255,255)
            pdf.set_text_color(24,29,31)
            total = tot_presu1 + tot_presu2
            pdf.cell(160,4,"Total".decode("UTF-8"),'LTBR',0,'L',1)
            pdf.cell(25,4,"Bs. "+str(total),'LTBR',1,'R',1)
            pdf.set_fill_color(255,255,255)
                            
            ############ Fin Proyecto ########################
                    
            ############ Partidas Accion Centralizda ########################
            
            #    #~ ############################################################################################################
            #    #~ ############################################### PAGINA 2####################################################
            #    #~ ############################################################################################################
            tot_acc1 = 0
            cr.execute('SELECT COUNT(tpa.id) AS cantidad FROM accion_centralizada AS ac INNER JOIN tipo_accion_centralizada AS tpa ON ac.n_accion_centra=tpa.id WHERE ac.organismo='+str(id_ente)+' AND ac.estatus=\'4\' AND ac.monto_asignado > 0') 
            for aprobadas in cr.fetchall():
                tot_acc1 = aprobadas[0]
                
                
                if tot_acc1 > 0:
                    t = 1
                    
                    pdf.alias_nb_pages() # LLAMADA DE PAGINACION
                    pdf.add_page() # AÑADE UNA NUEVA PAGINACION
                    #pdf.set_font('Times','',10) # TAMAÑO DE LA FUENTE
                    pdf.set_font('Arial','B',15)
                    pdf.set_fill_color(157,188,201) # COLOR DEL BORDE DE LA CELDA
                    pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
                    pdf.set_margins(20,5,10) # MARGEN DEL DOCUMENTO
                    #pdf.ln(20) # Saldo de linea
                    # 10 y 50 eje x y y 200 dimencion
                    #pdf.line(10, 40, 200, 40) Linea 
                    pdf.set_line_width(0.5)
                    
                    pdf.set_line_width(0.25)
                    pdf.set_y(58)
                    pdf.set_x(20)
                    pdf.line(20, 73, 20, 258)
                    #~ pdf.line(20, 260, 205, 260)
                    pdf.line(205, 258, 205, 73 )
                     
                    pdf.set_fill_color(234,233,229)
                    pdf.set_text_color(24,29,31)
                    pdf.set_line_width(0.25)
                    pdf.set_font('Times','B',7)
                    pdf.set_y(50)
                    pdf.set_x(20)
                    pdf.ln(7)
                    pdf.cell(150,4,ente,'LTBR',0,'L',1)
                    pdf.cell(35,4,"LEY DE PRESUPUESTO "+str(fecha),'TR',1,'L',1)
                    
            cr.execute('SELECT DISTINCT tpa.id,tpa.a_centralizada FROM accion_centralizada AS ac INNER JOIN tipo_accion_centralizada AS tpa ON ac.n_accion_centra=tpa.id WHERE ac.estatus=\'4\' AND organismo='+str(id_ente)+' ORDER BY tpa.id')
            k=0
            j = 45
            for i in cr.fetchall():
                a_id           = i[0]
                a_centralizada = i[1]
                
                if( t <= tot_acc1):
                                    
                    pdf.multi_cell(185,4,"RESUMEN DE CRÉDITOS PRESUPUESTARIOS (EN BOLIVARES)".decode("UTF-8"),'LRTB','J',1)
                    pdf.multi_cell(185,4,"ACCIÓN CENTRALIZADA "+a_centralizada.encode("UTF-8").decode("UTF-8"),'LRTB','J',1)
                    pdf.multi_cell(185,4,"RESUMEN DE LAS ACCIONES CENTRALIZADAS (EN BOLIVARES)".decode("UTF-8"),'TLRB','J',1)
                    pdf.set_font('Times','B',5)
                    pdf.set_fill_color(249,240,204)
                    
                    pdf.set_y(73+k)
                    pdf.multi_cell(22,14,"PARTIDA DE EGRESO".decode("UTF-8"),'LTBR','C',1)
                    pdf.set_y(73+k)
                    pdf.set_x(42)
                    pdf.cell(38,14,"DENOMINACIÓN".decode("UTF-8"),'LRBT',0,'C',1)
                    pdf.cell(125,4,"FUENTE DE FINANCIAMIENTO".decode("UTF-8"),'LTRB',1,'C',1)
                    pdf.set_y(77+k)
                    pdf.set_x(80)
                    pdf.multi_cell(25,5,"SITUADO CONSTITUCIONAL".decode("UTF-8"),'BLTR','C',1)
                    pdf.set_y(77+k)
                    pdf.set_x(102)
                    pdf.multi_cell(15,5,"GESTIÓN FISCAL".decode("UTF-8"),'LTRB','C',1)
                    pdf.set_y(77+k)
                    pdf.set_x(117)
                    pdf.multi_cell(28,5,"FONDO DE COMPENSACIÓN INTERTERRITORIAL".decode("UTF-8"),'LTRB','C',1)
                    pdf.set_y(77+k)
                    pdf.set_x(145)
                    pdf.multi_cell(35,5,"TRANSFERENCIAS CORRIENTES INTERNAS DE LA REPÚBLICA".decode("UTF-8"),'LTRB','C',1)
                    pdf.set_y(77+k)
                    pdf.set_x(180)
                    pdf.multi_cell(25,5,"TOTAL PRESUPUESTO "+str(fecha),'LTRB','C',1)
                    
                    
                    tot_part = 0
                    cr.execute('SELECT COUNT(iac.imputacion_acc_ids) AS cantidad FROM imputacion_accion_centralizada AS iac INNER JOIN partida_presupuestaria AS pp ON iac.partida_presu=pp.id INNER JOIN accion_centralizada AS ac ON iac.imputacion_acc_ids=ac.id INNER JOIN tipo_accion_centralizada AS tpa ON ac.n_accion_centra=tpa.id WHERE ac.organismo='+str(id_ente)+' AND ac.estatus=\'4\' AND iac.monto_asignado > 0 AND tpa.id='+str(a_id)) 
                    for rtotal in cr.fetchall():
                        tot_part = rtotal[0]
                    
                    
                    i = 1
                    
                    
                    cr.execute('SELECT DISTINCT iac.codigo, pp.partida, iac.monto_asignado FROM imputacion_accion_centralizada AS iac INNER JOIN partida_presupuestaria AS pp ON iac.partida_presu=pp.id INNER JOIN accion_centralizada AS ac ON iac.imputacion_acc_ids=ac.id INNER JOIN tipo_accion_centralizada AS tpa ON ac.n_accion_centra=tpa.id WHERE ac.organismo='+str(id_ente)+' AND ac.estatus=\'4\' AND iac.monto_asignado > 0 AND tpa.id='+str(a_id)+' AND iac.codigo != \'4.07\' ORDER BY iac.codigo') 
                    montot = 0.00
                    for resumenacc in cr.fetchall():
                    
                        codigo         = resumenacc[0]
                        monto_sc       = 0.00
                        monto_gf       = 0.00
                        monto_fci      = 0.00
                        monto_tci      = 0.00
                        partida        = resumenacc[1]
                        monto_asignado = resumenacc[2]
                    
                        if( i <= tot_part):
                    
                            pdf.set_fill_color(255,255,255)
                            pdf.set_font('Times','',7)
                            
                            if fuente_fin == "1":
                                monto_sc=monto_asignado
                            if fuente_fin == "2":
                                monto_gf=monto_asignado
                            if fuente_fin == "3":
                                monto_fci=monto_asignado
                            if fuente_fin == "4":
                                monto_tci=monto_asignado
                                    
                            if codigo!="4.07":
                                pdf.cell(22,4,str(codigo),'L',0,'L',1)
                                pdf.multi_cell(38,4,partida.encode("UTF-8").decode("UTF-8"),0,'J',1)
                
                                pdf.set_x(85)
                                montot=monto_sc+monto_gf+monto_fci+monto_tci    
                                pdf.cell(17,4,str(monto_sc),0,0,'R',1)
                                pdf.cell(15,4,str(monto_gf),0,0,'R',1)
                                pdf.cell(28,4,str(monto_fci),0,0,'R',1)
                                pdf.cell(35,4,str(monto_tci),0,0,'R',1)
                                pdf.cell(25,4,str(montot),'R',1,'R',1)
                    i = i+1
                        
                    pdf.set_fill_color(234,233,229)
                    
                    pdf.set_font('Times','B',7)
                    
                    pdf.set_y(por_y+j)
                    j = j + 10
                    k = k + 53
                    
                    tot_part1 = 0
                    cr.execute('SELECT COUNT(iac.imputacion_acc_ids) AS cantidad FROM imputacion_accion_centralizada AS iac INNER JOIN partida_presupuestaria AS pp ON iac.partida_presu=pp.id INNER JOIN accion_centralizada AS ac ON iac.imputacion_acc_ids=ac.id INNER JOIN tipo_accion_centralizada AS tpa ON ac.n_accion_centra=tpa.id WHERE ac.organismo='+str(id_ente)+' AND iac.monto_asignado > 0 AND tpa.id='+str(a_id)+' AND  iac.codigo = \'4.07\'') 
                    for rtotal1 in cr.fetchall():
                        tot_part1 = rtotal1[0]
                    
                    
                    i = 1
                    
                    cr.execute('SELECT DISTINCT iac.codigo, pp.partida, iac.monto_asignado FROM imputacion_accion_centralizada AS iac INNER JOIN partida_presupuestaria AS pp ON iac.partida_presu=pp.id  INNER JOIN accion_centralizada AS ac ON iac.imputacion_acc_ids=ac.id  INNER JOIN tipo_accion_centralizada AS tpa ON ac.n_accion_centra=tpa.id  WHERE ac.organismo=16  AND ac.estatus=\'4\' AND iac.monto_asignado > 0 AND tpa.id=2  AND iac.codigo = \'4.07\' ORDER BY iac.codigo') 
                    montot = 0.00
                    for partidas in cr.fetchall():
                        codigo         = partidas[0]
                        monto_sc       = 0.00
                        monto_gf       = 0.00
                        monto_fci      = 0.00
                        monto_tci      = 0.00
                        partida        = partidas[1]
                        monto_asignado = partidas[2]
                        
                        if( i <= tot_part1):
                        
                            pdf.set_fill_color(234,233,229)
                            pdf.set_font('Times','B',7)
                            pdf.set_y(200)
                            pdf.multi_cell(185,4,"RELACIÓN DE TRANSFERENCIAS (EN BOLIVARES)".decode("UTF-8"),'TLRB','J',1)
                            pdf.set_font('Times','B',5)
                            pdf.set_fill_color(249,240,204)
                        
                            pdf.set_y(204)
                            pdf.multi_cell(22,14,"PARTIDA DE EGRESO".decode("UTF-8"),'LTBR','C',1)
                            pdf.set_y(204)
                            pdf.set_x(42)
                            pdf.cell(38,14,"DENOMINACIÓN".decode("UTF-8"),'LRBT',0,'C',1)
                            pdf.cell(125,4,"FUENTE DE FINANCIAMIENTO".decode("UTF-8"),'LTRB',1,'C',1)
                            pdf.set_y(208)
                            pdf.set_x(80)
                            pdf.multi_cell(25,5,"SITUADO CONSTITUCIONAL".decode("UTF-8"),'BLTR','C',1)
                            pdf.set_y(208)
                            pdf.set_x(102)
                            pdf.multi_cell(15,5,"GESTIÓN FISCAL".decode("UTF-8"),'LTRB','C',1)
                            pdf.set_y(208)
                            pdf.set_x(117)
                            pdf.multi_cell(28,5,"FONDO DE COMPENSACIÓN INTERTERRITORIAL".decode("UTF-8"),'LTRB','C',1)
                            pdf.set_y(208)
                            pdf.set_x(145)
                            pdf.multi_cell(35,5,"TRANSFERENCIAS CORRIENTES INTERNAS DE LA REPÚBLICA".decode("UTF-8"),'LTRB','C',1)
                            pdf.set_y(208)
                            pdf.set_x(180)
                            pdf.multi_cell(25,5,"TOTAL PRESUPUESTO "+str(fecha),'LTRB','C',1)
                            
                            pdf.set_fill_color(255,255,255)
                            pdf.set_font('Times','',7)
                                
                            if fuente_fin == "1":
                                monto_sc=monto_asignado
                            if fuente_fin == "2":
                                monto_gf=monto_asignado
                            if fuente_fin == "3":
                                monto_fci=monto_asignado
                            if fuente_fin == "4":
                                monto_tci=monto_asignado
                                    
                            pdf.cell(22,4,str(codigo),'L',0,'L',1)
                            pdf.multi_cell(38,4,partida.encode("UTF-8").decode("UTF-8"),0,'J',1)
                
                            pdf.set_x(85)
                
                            montot=monto_sc+monto_gf+monto_fci+monto_tci    
                            pdf.cell(17,4,str(monto_sc),0,0,'R',1)
                            pdf.cell(15,4,str(monto_gf),0,0,'R',1)
                            pdf.cell(28,4,str(monto_fci),0,0,'R',1)
                            pdf.cell(35,4,str(monto_tci),0,0,'R',1)
                            pdf.cell(25,4,str(montot),'R',1,'R',1)
            
            pdf.set_fill_color(255,255,255)        
            pdf.set_y(255)
            pdf.set_x(20)
            pdf.cell(185,4,"".decode("UTF-8"),'LBR',1,'C',1)
            
            ############ Fin Partidas Acciones Centralizadas ########################

            ############ Partidas Proyectos ########################
            
            ###~ ############################################################################################################
            ###~ ############################################### PAGINA 3####################################################
            ###~ ############################################################################################################
            if tot_proy > 0:
                
                pdf.alias_nb_pages() # LLAMADA DE PAGINACION
                pdf.add_page() # AÑADE UNA NUEVA PAGINACION
                #pdf.set_font('Times','',10) # TAMAÑO DE LA FUENTE
                pdf.set_font('Arial','B',15)
                pdf.set_fill_color(157,188,201) # COLOR DEL BORDE DE LA CELDA
                pdf.set_text_color(24,29,31) # COLOR DEL TEXTO
                pdf.set_margins(20,5,10) # MARGEN DEL DOCUMENTO
                #pdf.ln(20) # Saldo de linea
                # 10 y 50 eje x y y 200 dimencion
                #pdf.line(10, 40, 200, 40) Linea 
                pdf.set_line_width(0.5)
                
                pdf.set_line_width(0.25)
                pdf.set_y(58)
                pdf.set_x(20)
                pdf.line(20, 73, 20, 258)
                #~ pdf.line(20, 260, 205, 260)
                pdf.line(205, 258, 205, 73 )
                
                pdf.set_fill_color(234,233,229)
                pdf.set_text_color(24,29,31)
                pdf.set_line_width(0.25)
                pdf.set_font('Times','B',7)
                pdf.set_y(50)
                pdf.set_x(20)
                pdf.ln(7)
                pdf.cell(150,4,ente,'LTBR',0,'L',1)
                pdf.cell(35,4,"LEY DE PRESUPUESTO "+str(fecha),'TRB',1,'L',1)
            
            cr.execute('SELECT op.estruc_presu, op.nombre_pro, pc.obj_general, oh.objetivo_historico, ona.objetivo_nacional, oes.objetivo_estrategico, oge.objetivo_general, les.lineas_estrategicas FROM proyecto_conaplan AS pc INNER JOIN observacion_proyecto AS op ON pc.id=op.codigo INNER JOIN objetivo_historico AS oh ON pc.obj_historico=oh.id  INNER JOIN objetivo_nacional AS ona ON pc.obj_nacional=ona.id  INNER JOIN objetivo_estrategico AS oes ON pc.obj_estrategico=oes.id  INNER JOIN objetivo_general AS oge ON pc.obj_general_plan=oge.id  INNER JOIN lineas_estrategicas AS les ON pc.linea_estrategica=les.id  WHERE ente='+str(id_ente)+' AND pc.estatus=\'4\'') 
            for resu_pro in cr.fetchall():
                estruc_presu               = resu_pro[0]
                nombre_pro                 = resu_pro[1]
                obj_general                = resu_pro[2]
                objetivo_historico         = resu_pro[3]
                objetivo_nacional          = resu_pro[4]
                objetivo_estrategico       = resu_pro[5]
                objetivo_general           = resu_pro[6]
                lineas_estrategicas        = resu_pro[7]
                
                if estruc_presu != None:
                
                    pdf.set_fill_color(255,255,255)
                    pdf.set_font('Times','B',7)
                    pdf.cell(185,4,"ESTRUCTURA PRESUPUESTARIA".decode("UTF-8"),'LR',1,'J',1)
                    pdf.set_font('Times','',8)
                    pdf.multi_cell(185,4,str(estruc_presu),'LR',0,'J',0)
                    pdf.set_font('Times','B',7)
                    pdf.cell(185,4,"PROYECTO".decode("UTF-8"),'LR',1,'J',1)
                    pdf.set_font('Times','',8)
                    pdf.multi_cell(185,4,nombre_pro.decode("UTF-8"),'LR','J',0)
                    pdf.set_font('Times','B',7)
                    pdf.multi_cell(185,4,"OBJETIVO GENERAL DEL PROYECTO".decode("UTF-8"),'LR','J',1)
                    pdf.set_font('Times','',8)
                    pdf.multi_cell(185,4,obj_general.decode("UTF-8"),'LR','J',1)
                    pdf.set_font('Times','B',7)
                    pdf.multi_cell(185,4,"OBJETIVO HISTÓRICO".decode("UTF-8"),'LR','J',1)
                    pdf.set_font('Times','',8)
                    pdf.multi_cell(185,4,objetivo_historico.decode("UTF-8"),'LR','J',1)
                    pdf.set_font('Times','B',7)
                    pdf.multi_cell(185,4,"OBJETIVO NACIONAL".decode("UTF-8"),'LR','J',1)
                    pdf.set_font('Times','',8)
                    pdf.multi_cell(185,4,objetivo_nacional.decode("UTF-8"),'LR','J',1)
                    pdf.set_font('Times','B',7)
                    pdf.multi_cell(185,4,"OBJETIVO ESTRATÉGICO".decode("UTF-8"),'LR','J',1)
                    pdf.set_font('Times','',8)
                    pdf.multi_cell(185,4,objetivo_estrategico.decode("UTF-8"),'LR','J',1)
                    pdf.set_font('Times','B',7)
                    pdf.multi_cell(185,4,"OBJETIVO GENERAL".decode("UTF-8"),'LR','J',1)
                    pdf.set_font('Times','',8)
                    pdf.multi_cell(185,4,objetivo_general.decode("UTF-8"),'LR','J',1)
                    pdf.set_font('Times','B',7)
                    pdf.multi_cell(185,4,"LÍNEA ESTRÁTEGICA DEL PLAN DE GOBIERNO".decode("UTF-8"),'LR','L',1)
                    pdf.set_font('Times','',8)
                    pdf.multi_cell(185,4,lineas_estrategicas.decode("UTF-8"),'LR','L',1)
            
                    pdf.set_font('Times','B',7)
                    pdf.set_fill_color(234,233,229)
                    pdf.multi_cell(185,4,"RESUMEN DE CRÉDITOS PRESUPUESTARIOS (EN BOLIVARES)".decode("UTF-8"),'TLRB','J',1)
                    pdf.set_font('Times','B',5)
                    pdf.set_fill_color(249,240,204)
                     
                    pdf.multi_cell(22,7,"PARTIDA PRESUPUESTARIA".decode("UTF-8"),'LTBR','C',1)
                    pdf.set_y(137)
                    pdf.set_x(42)
                    pdf.cell(38,14,"DENOMINACIÓN".decode("UTF-8"),'LRBT',0,'C',1)
                    pdf.cell(125,4,"FUENTE DE FINANCIAMIENTO".decode("UTF-8"),'LTRB',1,'C',1)
                    pdf.set_y(141)
                    pdf.set_x(80)
                    pdf.multi_cell(25,5,"SITUADO CONSTITUCIONAL".decode("UTF-8"),'LTRB','C',1)
                    pdf.set_y(141)
                    pdf.set_x(102)
                    pdf.multi_cell(15,5,"GESTIÓN FISCAL".decode("UTF-8"),'LTRB','C',1)
                    pdf.set_y(141)
                    pdf.set_x(117)
                    pdf.multi_cell(28,5,"FONDO DE COMPENSACIÓN INTERTERRITORIAL".decode("UTF-8"),'LTRB','C',1)
                    pdf.set_y(141)
                    pdf.set_x(145)
                    pdf.multi_cell(35,5,"TRANSFERENCIAS CORRIENTES INTERNAS DE LA REPÚBLICA".decode("UTF-8"),'LTRB','C',1)
                    pdf.set_y(141)
                    pdf.set_x(180)
                    pdf.multi_cell(25,5,"TOTAL PRESUPUESTO 2015".decode("UTF-8"),'LTRB','C',1)	 
                    
                    pdf.set_fill_color(255,255,255)
                    #pdf.ln(5)
            
            cr.execute('SELECT DISTINCT ip.codigo, pp.partida, ip.monto_asignado FROM imputacion_presupuestaria AS ip INNER JOIN partida_presupuestaria AS pp ON ip.partida_presu=pp.id INNER JOIN proyecto_conaplan AS pc ON ip.imputacion_ids=pc.id WHERE pc.organismo='+str(id_ente)+' AND pc.estatus=\'4\' ORDER BY ip.codigo') 
            montot     = 0.00
            tot_proyec = 0.00
            fuente_fin2 = 0
            for par_proy in cr.fetchall():
                    
                codigo         = par_proy[0]
                monto_sc       = 0.00
                monto_gf       = 0.00
                monto_fci      = 0.00
                monto_tci      = 0.00
                partida        = par_proy[1]
                monto_asignado = par_proy[2]
                
                if fuente_fin == "1" or fuente_fin2 =="1":
                    monto_sc=monto_asignado
                if fuente_fin == "2" or fuente_fin2 =="2":
                    monto_gf=monto_asignado
                if fuente_fin == "3":
                    monto_fci=monto_asignado
                if fuente_fin == "4":
                    monto_tci=monto_asignado
                
                pdf.set_font('Times','',7)
                pdf.cell(22,4,str(codigo),'L',0,'L',1)
                pdf.multi_cell(38,4,partida.encode("UTF-8").decode("UTF-8"),0,'J',1)
                    
                #pdf.set_y(169)
                pdf.set_x(85)
                
                montot=monto_sc+monto_gf+monto_fci+monto_tci
                pdf.cell(17,4,str(monto_sc),'',0,'R',1)
                pdf.cell(15,4,str(monto_gf),'',0,'R',1)
                pdf.cell(28,4,str(monto_fci),'',0,'R',1)
                pdf.cell(35,4,str(monto_tci),'',0,'R',1)
                pdf.cell(25,4,str(montot),'R',1,'R',1)
                tot_proyec+=montot
            
            pdf.set_y(255)
            pdf.set_x(20)
            pdf.set_font('Times','B',7)
            pdf.cell(160,4,"Monto Total de Proyecto".decode("UTF-8"),'LTBR',0,'L',1)
            pdf.cell(25,4,"Bs. "+str(tot_proyec),'LTBR',1,'R',1)

        
        nom = "Ley Presupuestaria "+str(fecha)+'.pdf'
        
    
        
        ruta_fun = ruta('')
        pdf.output(ruta_fun+'/reportes/'+nom,'F')
        #pdf.output('/home/administrador/openerp70/modules/planificacion_presupuesto/reportes/'+nom,'F')
        archivo = open(ruta_fun+'/reportes/'+nom)
        #archivo = open('/home/administrador/openerp70/modules/planificacion_presupuesto/reportes/'+nom)
        r_archivo = self.pool.get('reportes.generales').create(cr, uid, {
        'name' : nom,
        'res_name' : nom,
        'datas' : base64.encodestring(archivo.read()),
        'datas_fname' : nom,
        'res_model' : 'wizard.ley.presupuestaria',
        'registro': 'Resumen Ley Presupuestaria',
       },context=context)
                                 
    _columns = {
        #'acciones_ids':fields.many2one('proyecto.conaplan', 'acciones_especificas', ondelete='cascade', select=False),
        'year_fiscal': fields.selection([(num, str(num)) for num in range(2014, (datetime.now().year)+30 )], 'Año Fiscal', required=False),
        'sector':fields.many2one('organos.sectores', 'Sector', ondelete='cascade', select=False, required=False),

    }
    #los siguientes son metodos globales, los identifico porque estan pegados de la barra numeral del codigo
def acento(cadena):
    result = cadena.encode('UTF-8').decode('UTF-8')# INSTITUCION
    return result
wizard_resumen()
    
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

def ruta( usuario ):
    ruta = '/home'
    if usuario == 'administrador':
        ruta = '/home/administrador/openerp70/modules/planificacion_presupuesto'

    return ruta

