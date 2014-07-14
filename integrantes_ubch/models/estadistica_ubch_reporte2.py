# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
import clases_reportes
import unicodedata

def gen_est_centros_mun(cr, municipio):
	
	#Variables globales		
	j=0
	k=0
	item = 0
	F_totales = 0
	M_totales = 0
	TCD_totales = 0
	FCD_totales = 0
	PCC_totales = 0
	total_integrantes = 0
	
	#Modelos
	modelo_integrantes = "integrantes_ubch"
	modelo_centros = "integrante_centroelectoral"
	modelo_familiares = "grupo_familiar"
	modelo_municipios = "res_country_municipality"
	
	# Instancia de la clase heredada L es horizontal y P es vertical
	pdf=clases_reportes.PDF(orientation='L',unit='mm',format='letter') #HORIENTACION DE LA PAGINA
	
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
	pdf.set_line_width(0.25)
	
	#~ print "Municipio: " + str(municipio)
	
	#Cosultamos el modelo de los municipios para obtener el nombre del municipio correspondiente
	cr.execute('SELECT name FROM '+modelo_municipios+' WHERE id = '+str(municipio))
	mun = cr.fetchone()[0]

	pdf.set_fill_color(199,15,15)
	pdf.set_text_color(255,255,255)
	pdf.cell(7,5,"#",'LTBR',0,'C',1)
	pdf.set_font('Arial','B',11)
	pdf.cell(143,5,"Centro Electoral (Municipio: "+mun+")".decode("UTF-8"),'LTBR',0,'C',1)
	pdf.cell(15,5,"F".decode("UTF-8"),'LTBR',0,'C',1)
	pdf.cell(15,5,"M".decode("UTF-8"),'LTBR',0,'C',1)
	pdf.cell(15,5,"TCD".decode("UTF-8"),'LTBR',0,'C',1)
	pdf.cell(15,5,"FCD".decode("UTF-8"),'LTBR',0,'C',1)
	pdf.cell(20,5,"PCC".decode("UTF-8"),'LTBR',0,'C',1)
	pdf.cell(25,5,"Total p/ C.E.".decode("UTF-8"),'LTBR',1,'C',1)
	pdf.set_fill_color(255,255,255)
	pdf.set_text_color(24,29,31)
	
	#Cosultamos los bancos
	cr.execute('SELECT id, centro FROM '+modelo_centros)
	for centros in cr.fetchall():
		#~ print "Centro: "+str(centros[0])+"-"+centros[1].encode("UTF-8").decode("UTF-8")
		centro = centros[1].encode("UTF-8").decode("UTF-8")
		F = 0 #Titulares femeninos 
		M = 0 #Titulares masculinos
		TCD = 0 #Titulares con discapacidad
		FCD = 0 #Familiares con discapacidad
		PCC = 0 #Titulares pertenecientes a un Cosejo Comunal
		integrantes_centro = 0
		
		#Consultar todos los registros femeninos para el centro de votación especificado
		cr.execute("SELECT count(*) as F FROM "+modelo_integrantes+" WHERE municipio = "+str(municipio)+" AND centro_votacion = "+str(centros[0])+" AND sexo = '1'")
		F = cr.fetchone()[0]
		#Consultar todos los registros masculinos para el centro de votación especificado
		cr.execute("SELECT count(*) as M FROM "+modelo_integrantes+" WHERE municipio = "+str(municipio)+" AND centro_votacion = "+str(centros[0])+" AND sexo = '2'")
		M = cr.fetchone()[0]
		#Consultar todos los registros con discapacidad para el centro de votación especificado
		cr.execute("SELECT count(*) as disc FROM "+modelo_integrantes+" WHERE municipio = "+str(municipio)+" AND centro_votacion = "+str(centros[0])+" AND discapacidad = '1'")
		TCD = cr.fetchone()[0]
		#Consultar todos los registros para el centro de votación especificado, los cuales tengan familiares con discapacidad
		cr.execute('SELECT id FROM '+modelo_integrantes+' WHERE municipio = '+str(municipio)+' AND centro_votacion = '+str(centros[0]))
		for integrante in cr.fetchall():
			id_integ = integrante[0]
			print id_integ
			cr.execute("SELECT count(*) as fam_disc FROM "+modelo_familiares+" WHERE integrante = "+str(id_integ)+" AND discapacidad = '1'")
			FCD = cr.fetchone()[0]
		#Consultar todos los registros pertenecientes a un consejo comunal para el centro de votación especificado
		cr.execute("SELECT count(*) as i_c FROM "+modelo_integrantes+" WHERE municipio = "+str(municipio)+" AND centro_votacion = "+str(centros[0])+" AND consejo_cumunal = TRUE")
		PCC = cr.fetchone()[0]
		
		#Reasignaciones
		integrantes_centro = F + M
		F_totales = F_totales + F
		M_totales = M_totales + M
		TCD_totales = TCD_totales + TCD
		FCD_totales = FCD_totales + FCD
		PCC_totales = PCC_totales + PCC
		total_integrantes = total_integrantes + integrantes_centro
		
		if j == 24:
			pdf.add_page()
			pdf.set_fill_color(199,15,15)
			pdf.set_text_color(255,255,255)
			pdf.set_font('Arial','B',11)
			pdf.cell(150,5,"Centro Electoral (Municipio: "+mun+")".decode("UTF-8"),'LTBR',0,'C',1)
			pdf.cell(15,5,"F",'LTBR',0,'C',1)
			pdf.cell(15,5,"M",'LTBR',0,'C',1)
			pdf.cell(15,5,"TCD",'LTBR',0,'C',1)
			pdf.cell(15,5,"FCD",'LTBR',0,'C',1)
			pdf.cell(20,5,"PCC",'LTBR',0,'C',1)
			pdf.cell(25,5,"Total p/ C.E.",'LTBR',1,'C',1)
			pdf.set_fill_color(255,255,255)
			pdf.set_text_color(24,29,31)	
					
			j=0
			
		pdf.set_fill_color(191,191,191)
		pdf.set_text_color(24,29,31)
		pdf.set_font('Arial','B',8)
		item = int(item) + 1
		pdf.cell(7,5,str(item),'LTBR',0,'L',1)
		pdf.cell(143,5,centro,'LTBR',0,'L',1)
		pdf.set_fill_color(255,255,255)
		pdf.set_text_color(24,29,31)
		pdf.set_font('Arial','',8)
		pdf.cell(15,5,str(F),'LTBR',0,'C',1)
		pdf.cell(15,5,str(M),'LTBR',0,'C',1)
		pdf.cell(15,5,str(TCD),'LTBR',0,'C',1)
		pdf.cell(15,5,str(FCD),'LTBR',0,'C',1)
		pdf.cell(20,5,str(PCC),'LTBR',0,'C',1)
		pdf.cell(25,5,str(integrantes_centro),'LTBR',1,'C',1)
		
		if k == 24:
			pdf.set_fill_color(97,97,97)
			pdf.set_text_color(255,255,255)
			pdf.set_font('Arial','B',8)
			pdf.cell(150,5,"TOTALES".decode("UTF-8"),'LTBR',0,'L',1)
			pdf.cell(15,5,str(F_totales),'LTBR',0,'C',1)
			pdf.cell(15,5,str(M_totales),'LTBR',0,'C',1)
			pdf.cell(15,5,str(TCD_totales),'LTBR',0,'C',1)
			pdf.cell(15,5,str(FCD_totales),'LTBR',0,'C',1)
			pdf.cell(20,5,str(PCC_totales),'LTBR',0,'C',1)
			pdf.cell(25,5,str(total_integrantes),'LTBR',1,'C',1)
			pdf.set_fill_color(255,255,255)
			pdf.set_text_color(24,29,31)
			pdf.line(10, 189, 265, 189) 
			pdf.set_y(190)
			pdf.set_x(10)
			pdf.set_text_color(110,108,108)
			pdf.set_font('Arial','B',8)
			pdf.cell(15,5,"Leyenda:".decode("UTF-8"),'',0,'C',1)
			pdf.set_font('Arial','',8)
			pdf.cell(185,5,"Femenino (F), Masculino (M), Titulares con Discapacidad (TCD), Familiares con de Discapacidad (FCD), Pertenecientes a un Cosejo Comunal (PCC), Total por Centro Electoral (Total p/ C.E.)".decode("UTF-8"),'',1,'L',1)
			k = 0
		j = j+1
		k = k+1
		
	pdf.set_fill_color(97,97,97)
	pdf.set_text_color(255,255,255)
	pdf.set_font('Arial','B',8)
	pdf.cell(150,5,"TOTALES",'LTBR',0,'L',1)
	pdf.cell(15,5,str(F_totales),'LTBR',0,'C',1)
	pdf.cell(15,5,str(M_totales),'LTBR',0,'C',1)
	pdf.cell(15,5,str(TCD_totales),'LTBR',0,'C',1)
	pdf.cell(15,5,str(FCD_totales),'LTBR',0,'C',1)
	pdf.cell(20,5,str(PCC_totales),'LTBR',0,'C',1)
	pdf.cell(25,5,str(total_integrantes),'LTBR',1,'C',1)
	pdf.set_fill_color(255,255,255)
	pdf.set_text_color(24,29,31)

	pdf.ln(10)

	#~ pdf.set_fill_color(97,97,97)
	#~ pdf.set_text_color(255,255,255)
	#~ pdf.set_font('Arial','B',8)
	#~ pdf.cell(180,5,"TOTAL".decode("UTF-8"),'LTBR',1,'C',1)
	#~ pdf.cell(15,5,"F".decode("UTF-8"),'LTBR',0,'C',1)
	#~ pdf.set_fill_color(255,255,255)
	#~ pdf.set_text_color(24,29,31)
	#~ pdf.cell(15,5,str(F_totales),'LTBR',0,'C',1)
	#~ pdf.set_fill_color(97,97,97)
	#~ pdf.set_text_color(255,255,255)
	#~ pdf.cell(15,5,"M".decode("UTF-8"),'LTBR',0,'C',1)
	#~ pdf.set_fill_color(255,255,255)
	#~ pdf.set_text_color(24,29,31)
	#~ pdf.cell(15,5,str(M_totales),'LTBR',0,'C',1)
	#~ pdf.set_fill_color(97,97,97)
	#~ pdf.set_text_color(255,255,255)
	#~ pdf.cell(15,5,"TCD".decode("UTF-8"),'LTBR',0,'C',1)
	#~ pdf.set_fill_color(255,255,255)
	#~ pdf.set_text_color(24,29,31)
	#~ pdf.cell(15,5,str(TCD_totales),'LTBR',0,'C',1)
	#~ pdf.set_fill_color(97,97,97)
	#~ pdf.set_text_color(255,255,255)
	#~ pdf.cell(15,5,"FCD".decode("UTF-8"),'LTBR',0,'C',1)
	#~ pdf.set_fill_color(255,255,255)
	#~ pdf.set_text_color(24,29,31)
	#~ pdf.cell(15,5,str(FCD_totales),'LTBR',0,'C',1)
	#~ pdf.set_fill_color(97,97,97)
	#~ pdf.set_text_color(255,255,255)
	#~ pdf.cell(15,5,"PCC".decode("UTF-8"),'LTBR',0,'C',1)
	#~ pdf.set_fill_color(255,255,255)
	#~ pdf.set_text_color(24,29,31)
	#~ pdf.cell(15,5,str(PCC_totales),'LTBR',0,'C',1)
	#~ pdf.set_fill_color(97,97,97)
	#~ pdf.set_text_color(255,255,255)
	#~ pdf.cell(15,5,"TOTAL".decode("UTF-8"),'LTBR',0,'C',1)
	#~ pdf.set_fill_color(255,255,255)
	#~ pdf.set_text_color(24,29,31)
	#~ pdf.cell(15,5,str(total_integrantes),'LTBR',0,'C',1)
	#~ pdf.set_fill_color(255,255,255)
	#~ pdf.set_text_color(24,29,31)



	pdf.line(10, 189, 265, 189) 
	pdf.set_y(190)
	pdf.set_x(10)
	pdf.set_text_color(110,108,108)
	pdf.set_font('Arial','B',8)
	pdf.cell(15,5,"Leyenda:".decode("UTF-8"),'',0,'C',1)
	pdf.set_font('Arial','',8)
	pdf.cell(185,5,"Femenino (F), Masculino (M), Titulares con Discapacidad (TCD), Familiares con Discapacidad (FCD), Pertenecientes a un Cosejo Comunal (PCC), Total por Centro Electoral (Total p/ C.E.)".decode("UTF-8"),'',1,'L',1)



	#Nombre del archivo
	nombre_archivo = 'estadisticas_ubch'+time.strftime('(%d-%m-%y)')+'.pdf'
	#Ruta local
	#~ pdf.output('openerp/addons/integrantes_ubch/reportes/estadisticas/'+nombre_archivo,'F')
	#~ archivo = open('openerp/addons/integrantes_ubch/reportes/estadisticas/'+nombre_archivo)
	#Ruta servidor
	pdf.output('/home/administrador/openerp70/modules/integrnates_ubch/reportes/estadisticas/'+nombre_archivo,'F')
	archivo = open('/home/administrador/openerp70/modules/integrantes_ubch/reportes/estadisticas/'+nombre_archivo)
	
	return nombre_archivo, archivo

