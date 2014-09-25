# -*- coding: utf-8 -*-
import time # Necesario para las funciones de Fecha
import class_pdf
import enletras #Esta librería recibe una cifra en el formato '0000000,00'

def gen_orden(dicc):
	#Genración del año correspondiente
	anyo = dicc['fecha_pago'].split('-') 
	anyo = anyo[0] #Año presupuestario
	
	#Validación de datos recibidos
	if not dicc['nombre_cesionado']:
		nom_ces = dicc['beneficiario_name']
	else:
		nom_ces = dicc['nombre_cesionado']
		
	if not dicc['cedula_cesionado']:
		ced_ces = dicc['cedula']
	else:
		ced_ces = dicc['cedula_cesionado']
		
	#Calculo del monto total de las imputaciones
	monto_total = 0.0
	MONTO = 0.0
	for linea in dicc['compromisos']:
		if not linea.monto_causar:
			MONTO = 0.0
		else:
			monto_total = float(monto_total + float(linea.monto_causar)) #Primero, transformamos todo el resultado a flotante
			MONTO = class_pdf.punto_decimal(str(class_pdf.decimal(monto_total))) #Luego, redondeamos los dígitos decimales y le damos el formato '000.000,00'
			print MONTO.replace('','')
		
	# Instancia de la clase heredada L es horizontal y P es vertical
	pdf=class_pdf.PDF(orientation='P',unit='mm',format='letter') #HORIENTACIÓN DE LA PÁGINA

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

	pdf.line(10, 37, 10, 215)  #LINEA DE MARGEN IZQUIERDO
	pdf.line(201, 37, 201, 215)  #LINEA DE MARGEN DERECHO

	pdf.line(17, 110, 17, 210)  #LINEA DE PROYECTO-ACCION
	pdf.line(24, 110, 24, 210)  #LINEA DE PARTIDA
	pdf.line(31, 110, 31, 210)  #LINEA DE GENERICA
	pdf.line(38, 110, 38, 210)  #LINEA DE ESPECIFICA
	pdf.line(57, 110, 57, 210)  #LINEA DE SUB-ESPECIFICA
	pdf.line(167, 110, 167, 210)  #LINEA DE DESCRIPCION


	pdf.set_fill_color(255,255,255)
	pdf.set_font('Arial','',7)
	pdf.set_y(0)
	pdf.set_x(62)
	pdf.write(30,"REPÚBLICA BOLIVARIANA DE VENEZUELA".decode("UTF-8"))
	pdf.set_y(3)
	pdf.set_x(62)
	pdf.write(30,"GOBIERNO DEL ESTADO ARAGUA".decode("UTF-8"))
	pdf.set_y(6)
	pdf.set_x(62)
	pdf.write(30,"A.C. BIBLIOTECAS VIRTUALES DE ARAGUA".decode("UTF-8"))

	pdf.set_y(13)
	pdf.set_x(161)
	pdf.multi_cell(40,4,"SOLICITUD".decode("UTF-8"),'LTR','C',0)
	pdf.set_y(17)
	pdf.set_x(161)
	pdf.multi_cell(40,4,"PRESUPUESTO"+str(anyo),'LBR','C',0)
	pdf.set_y(21)
	pdf.set_x(161)
	pdf.set_font('Arial','',5)
	pdf.multi_cell(40,2,"ORDEN".decode("UTF-8"),'LTR','L',0)
	pdf.set_y(23)
	pdf.set_x(161)
	pdf.set_font('Arial','B',8)
	pdf.multi_cell(40,4,str(dicc['num_pago']),'LBR','C',0)
	pdf.set_font('Arial','',7)
	pdf.set_y(27)
	pdf.set_x(161)
	pdf.set_font('Arial','',5)
	pdf.cell(30,2,"FECHA".decode("UTF-8"),'LTR',1,'L',0)
	pdf.set_y(27)
	pdf.set_x(191)
	pdf.cell(10,2,"PAG".decode("UTF-8"),'LTR',1,'L',0)
	pdf.set_y(29)
	pdf.set_x(161)
	pdf.set_font('Arial','B',8)
	pdf.cell(30,4,str(class_pdf.format_fecha(dicc['fecha_pago'])),'LBR',1,'C',0)
	pdf.set_y(29)
	pdf.set_x(191)
	pdf.cell(10,4,"1/1".decode("UTF-8"),'LBR',1,'C',0)
	pdf.set_y(27)
	pdf.set_x(50)
	pdf.set_font('Arial','B',11)
	pdf.multi_cell(110,6,"ORDEN DE PAGO".decode("UTF-8"),'','C',0)
	#~ pdf.write(30,"Pág: ".decode("UTF-8")+str(pdf.page_no())+"/"+str(pdf.alias_nb_pages()))

	pdf.ln(2)

	pdf.set_font('Arial','B',8)
	pdf.cell(191,4,"BENEFICIARIO".decode("UTF-8"),'LTBR',1,'C',1)
	pdf.set_font('Arial','',6)
	pdf.cell(160,3,"NOMBRE".decode("UTF-8"),'LTR',0,'L',1)
	pdf.cell(31,3,"NRO. DE R.I.F.".decode("UTF-8"),'LTR',1,'L',1)
	pdf.set_font('Arial','B',8)
	pdf.cell(160,4,dicc['beneficiario_name'].decode("UTF-8").upper(),'LBR',0,'L',1)
	pdf.cell(31,4,dicc['cedula'].decode("UTF-8"),'LBR',1,'C',1)
	pdf.cell(191,4,"AUTORIZADO A COBRAR CESIONARIO".decode("UTF-8"),'LTBR',1,'C',1)
	pdf.set_font('Arial','',6)
	pdf.cell(160,3,"NOMBRE".decode("UTF-8"),'LTR',0,'L',1)
	pdf.cell(31,3,"NRO. DE R.I.F.".decode("UTF-8"),'LTR',1,'L',1)
	pdf.set_font('Arial','B',8)
	pdf.cell(160,4,nom_ces.decode("UTF-8").upper(),'LBR',0,'L',1)
	pdf.cell(31,4,ced_ces.decode("UTF-8"),'LBR',1,'C',1)
	pdf.set_font('Arial','B',8)
	pdf.cell(191,4,"MONTO TOTAL".decode("UTF-8"),'LTBR',1,'C',1)
	pdf.set_font('Arial','',8)
	pdf.cell(160,6,enletras.en_letras(MONTO.replace('.',''), sep_decimal=',').decode("UTF-8").upper()+" CTMS",'LTB',0,'L',1)
	pdf.set_font('Arial','B',10)
	pdf.cell(31,6,"Bs. "+str(MONTO),'TBR',1,'R',1)
	pdf.set_font('Arial','',6)
	pdf.cell(191,4,"CONCEPTO".decode("UTF-8"),'LTR',1,'L',1)
	pdf.set_font('Arial','',8)
	pdf.multi_cell(191,5,dicc['observacion'].encode('UTF-8').decode("UTF-8").upper(),'LR','J',0)

	pdf.set_y(100)
	pdf.set_x(10)

	pdf.set_font('Arial','B',8)
	pdf.cell(191,4,"IMPUTACIÓN PRESUPUESTARIA".decode("UTF-8"),'LTBR',1,'C',1)

	pdf.set_y(104)
	pdf.set_x(10)
	pdf.set_font('Arial','',6)
	pdf.cell(7,4,"PROY",'LTBR',0,'C',1)
	pdf.cell(7,4,"ACC.",'LTBR',0,'C',1)
	pdf.cell(7,4,"".decode("UTF-8"),'LTBR',0,'C',1)
	pdf.cell(7,4,"".decode("UTF-8"),'LTBR',0,'C',1)
	pdf.cell(19,4,"PARTIDA".decode("UTF-8"),'LTBR',0,'C',1)
	pdf.set_font('Arial','',6)
	pdf.cell(110,4,"DESCRIPCION".decode("UTF-8"),'LTBR',0,'C',1)
	pdf.cell(34,4,"MONTO".decode("UTF-8"),'LTBR',1,'C',1)
	
	i = 0
	sub_total = 0.0
	for linea in dicc['compromisos']:
		#Sub-cadenas del código del proyecto
		split_codigo = linea.proyec_acc.split('-')
		
		split_a = split_codigo[0]
		split_b = split_codigo[1]
		split_c = split_codigo[2]
		split_d = split_codigo[3]
		
		pdf.cell(7,4,split_a,'LR',0,'C',1)
		pdf.cell(7,4,split_b,'LR',0,'C',1)
		pdf.cell(7,4,split_c,'LR',0,'C',1)
		pdf.cell(7,4,split_d,'LR',0,'C',1)
		pdf.cell(19,4,linea.partida.decode("UTF-8"),'LR',0,'C',1)
		pdf.set_font('Arial','',6)
		pdf.cell(110,4,linea.desc_partida.encode('UTF-8').decode("UTF-8"),'LR',0,'L',1)
		pdf.cell(34,4,str(linea.monto_causar),'LR',1,'R',1)

	pdf.set_y(210)
	pdf.set_x(10)
	pdf.set_font('Arial','',8)
	pdf.cell(157,4,"TOTAL        ".decode("UTF-8"),'LTB',0,'R',1)
	pdf.set_font('Arial','B',8)
	pdf.cell(34,4,str(MONTO),'TBR',1,'R',1)
	pdf.set_font('Arial','B',8)
	pdf.cell(191,4,"FIRMAS".decode("UTF-8"),'LTBR',1,'C',1)
	pdf.cell(95,4,"GERENCIA DE ADMINISTRACIÓN".decode("UTF-8"),'LTR',0,'L',1)
	pdf.cell(96,4,"GERENCIA DE PLANIFICACIÓN Y PRESUPUESTO".decode("UTF-8"),'LTR',1,'L',1)
	pdf.set_font('Arial','',8)
	pdf.cell(95,8,"".decode("UTF-8"),'LBR',0,'L',1)
	pdf.cell(96,8,"".decode("UTF-8"),'LBR',1,'L',1)

	pdf.set_font('Arial','B',8)
	pdf.cell(95,6,"TESORERIA".decode("UTF-8"),'LTR',0,'L',1)
	pdf.cell(96,6,"PRESIDENCIA".decode("UTF-8"),'LTR',1,'L',1)
	pdf.set_font('Arial','',8)
	pdf.cell(95,8,"".decode("UTF-8"),'LBR',0,'L',1)
	pdf.cell(96,8,"".decode("UTF-8"),'LBR',1,'L',1)
	pdf.set_font('Arial','B',6)
	pdf.cell(191,4,"RECIBO CONFORME".decode("UTF-8"),'LTBR',1,'C',1)
	pdf.set_font('Arial','',6)
	pdf.cell(65,3,"NOMBRE Y APELLIDOS".decode("UTF-8"),'LTR',0,'L',1)
	pdf.cell(50,3,"FIRMA".decode("UTF-8"),'LTR',0,'L',1)
	pdf.cell(40,3,"CEDULA DE IDENTIDAD N°".decode("UTF-8"),'LTR',0,'L',1)
	pdf.cell(36,3,"FECHA".decode("UTF-8"),'LTR',1,'L',1)
	pdf.cell(65,4,"".decode("UTF-8"),'LBR',0,'L',1)
	pdf.cell(50,4,"".decode("UTF-8"),'LBR',0,'L',1)
	pdf.cell(40,4,"".decode("UTF-8"),'LBR',0,'L',1)
	pdf.cell(36,4,"".decode("UTF-8"),'LBR',1,'L',1)
	pdf.cell(191,4,"ELABORADO POR T.S.U. DOMINGO PEREZ".decode("UTF-8"),'T',1,'L',1)
	pdf.ln(7)
	
	#Nombre del archivo
	nombre_archivo = "ORDEN_PAGO_"+str(dicc['num_pago'])+"_"+time.strftime('%d-%m-%y')+".pdf"
	#Ruta local
	#~ pdf.output('openerp/addons/tesoreria/reportes/ordenes_pago/'+nombre_archivo,'F')
	#~ archivo = open('openerp/addons/tesoreria/reportes/ordenes_pago/'+nombre_archivo)
	#Ruta servidor
	pdf.output('/home/administrador/openerp70/modules/tesoreria/reportes/ordenes_pago/'+nombre_archivo,'F')
	archivo = open('/home/administrador/openerp70/modules/tesoreria/reportes/ordenes_pago/'+nombre_archivo)

	return nombre_archivo, archivo
