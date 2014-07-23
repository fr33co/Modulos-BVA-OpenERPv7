# -*- coding: utf-8 -*-
from fpdf import FPDF

import fpdf

#title='Encabezado con estilo'

class PDF(FPDF):
	
	def header(self):
		#Arial bold 15
		self.set_font('Arial','B',15)
		
		# ALINEACION DE LA IMAGEN EN LA CABECERA DEL DOCUMENTO
		# (CAMPO 1 = HORIZONTAL , CAMPO 2 = VERTICAL, CAMPO 3 = DIMENCION DE LA IMAGEN)
		
		self.image('estadisticas.jpg',10,10,255)
		#Calcular ancho del texto (title) y establecer posición
		#w=self.get_string_width(title)+6
		#self.set_x((210-w)/2)
		#Colores del marco, fondo y texto
		self.set_draw_color(0,80,180)
		self.set_fill_color(28,108,198)
		self.set_text_color(220,50,50)
		#Grosor del marco (1 mm)
		#self.set_line_width(1)
		#Titulo
		#self.cell(w,9,title,1,1,'C',1)
		#Salto de línea
		self.ln(28)

		
		#METODO PARA CONSTRUIR LA PAGINACION
		# Page footer
	def footer(self):
		#Posición a 1.5 cm desde abajo
		self.set_y(-15)
		#Arial italic 8
		self.set_font('Arial','I',8)
		#Color de texto en gris
		self.set_text_color(128)
		#Numero de pagina
		self.cell(0,10,'Pagina '+str(self.page_no()),0,0,'R') 
		
	def chapter_title(self,num,label):
		#Arial 12
		self.set_font('Arial','',12)
		#Color de fondo
		self.set_fill_color(200,220,255)
		#Titulo
		self.cell(0,6,"Chapter %d : %s"%(num,label),0,1,'L',1)
		#Salto de línea
		self.ln(4)
		
	def chapter_body(self,name):
		#Leer archivo de texto
		txt=file(name).read()
		#Times 12
		self.set_font('Times','',12)
		#Emitir texto justificado
		self.multi_cell(0,5,txt)
		#Salto de línea
		self.ln()
		#Mención en italic -cursiva-
		self.set_font('','I')
		self.cell(0,5,'(end of excerpt)')
		
	# CONSTRUCCTOR DEL DOCUMENTO
	def print_chapter(self,num,title,name):
		self.add_page()
		self.chapter_title(num,title)
		self.chapter_body(name)

	
# Instancia de la clase heredada L es horizontal y P es vertical

pdf=PDF(orientation='L',unit='mm',format='letter') #HORIENTACION DE LA PAGINA

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

pdf.set_fill_color(199,15,15)
pdf.set_text_color(255,255,255)
pdf.cell(7,5,"#",'LTBR',0,'C',1)
pdf.set_font('Arial','B',11)
pdf.cell(143,5,"Centro Electoral".decode("UTF-8"),'LTBR',0,'C',1)
pdf.cell(15,5,"F".decode("UTF-8"),'LTBR',0,'C',1)
pdf.cell(15,5,"M".decode("UTF-8"),'LTBR',0,'C',1)
pdf.cell(15,5,"TCD".decode("UTF-8"),'LTBR',0,'C',1)
pdf.cell(15,5,"FCD".decode("UTF-8"),'LTBR',0,'C',1)
pdf.cell(20,5,"PCC".decode("UTF-8"),'LTBR',0,'C',1)
pdf.cell(25,5,"Total p/ C.E.".decode("UTF-8"),'LTBR',1,'C',1)
pdf.set_fill_color(255,255,255)
pdf.set_text_color(24,29,31)

j=0
k=0
item = 0
for i in range(1,80):
	
	if j == 24:
		pdf.add_page()
		pdf.set_fill_color(199,15,15)
		pdf.set_text_color(255,255,255)
		pdf.set_font('Arial','B',11)
		pdf.cell(150,5,"Centro Electoral".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(15,5,"F".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(15,5,"M".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(15,5,"TCD".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(15,5,"FCD".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(20,5,"PCC".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(25,5,"Total p/ C.E.".decode("UTF-8"),'LTBR',1,'C',1)
		pdf.set_fill_color(255,255,255)
		pdf.set_text_color(24,29,31)	
				
		j=0
		
	pdf.set_fill_color(191,191,191)
	pdf.set_text_color(24,29,31)
	pdf.set_font('Arial','B',8)
	item = int(item) + 1
	pdf.cell(7,5,str(item),'LTBR',0,'L',1)
	pdf.cell(143,5,"SOCORRO".decode("UTF-8"),'LTBR',0,'L',1)
	pdf.set_fill_color(255,255,255)
	pdf.set_text_color(24,29,31)
	pdf.set_font('Arial','',8)
	pdf.cell(15,5,"2200".decode("UTF-8"),'LTBR',0,'C',1)
	pdf.cell(15,5,"3000".decode("UTF-8"),'LTBR',0,'C',1)
	pdf.cell(15,5,"500".decode("UTF-8"),'LTBR',0,'C',1)
	pdf.cell(15,5,"25000".decode("UTF-8"),'LTBR',0,'C',1)
	pdf.cell(20,5,"12500".decode("UTF-8"),'LTBR',0,'C',1)
	pdf.cell(25,5,"12500".decode("UTF-8"),'LTBR',1,'C',1)
	
	if k == 23:
		pdf.set_fill_color(97,97,97)
		pdf.set_text_color(255,255,255)
		pdf.set_font('Arial','B',8)
		pdf.cell(150,5,"TOTALES".decode("UTF-8"),'LTBR',0,'L',1)
		pdf.cell(15,5,"22000".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(15,5,"30000".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(15,5,"5000".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(15,5,"250000".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(20,5,"12500".decode("UTF-8"),'LTBR',0,'C',1)
		pdf.cell(25,5,"12500".decode("UTF-8"),'LTBR',1,'C',1)
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
pdf.cell(150,5,"TOTALES".decode("UTF-8"),'LTBR',0,'L',1)
pdf.cell(15,5,"22000".decode("UTF-8"),'LTBR',0,'C',1)
pdf.cell(15,5,"30000".decode("UTF-8"),'LTBR',0,'C',1)
pdf.cell(15,5,"5000".decode("UTF-8"),'LTBR',0,'C',1)
pdf.cell(15,5,"250000".decode("UTF-8"),'LTBR',0,'C',1)
pdf.cell(20,5,"12500".decode("UTF-8"),'LTBR',0,'C',1)
pdf.cell(25,5,"12500".decode("UTF-8"),'LTBR',1,'C',1)
pdf.set_fill_color(255,255,255)
pdf.set_text_color(24,29,31)

pdf.ln(10)

pdf.set_fill_color(97,97,97)
pdf.set_text_color(255,255,255)
pdf.set_font('Arial','B',8)
pdf.cell(180,5,"TOTAL".decode("UTF-8"),'LTBR',1,'C',1)
pdf.cell(15,5,"F".decode("UTF-8"),'LTBR',0,'C',1)
pdf.set_fill_color(255,255,255)
pdf.set_text_color(24,29,31)
pdf.cell(15,5,"".decode("UTF-8"),'LTBR',0,'C',1)
pdf.set_fill_color(97,97,97)
pdf.set_text_color(255,255,255)
pdf.cell(15,5,"M".decode("UTF-8"),'LTBR',0,'C',1)
pdf.set_fill_color(255,255,255)
pdf.set_text_color(24,29,31)
pdf.cell(15,5,"".decode("UTF-8"),'LTBR',0,'C',1)
pdf.set_fill_color(97,97,97)
pdf.set_text_color(255,255,255)
pdf.cell(15,5,"TCD".decode("UTF-8"),'LTBR',0,'C',1)
pdf.set_fill_color(255,255,255)
pdf.set_text_color(24,29,31)
pdf.cell(15,5,"0".decode("UTF-8"),'LTBR',0,'C',1)
pdf.set_fill_color(97,97,97)
pdf.set_text_color(255,255,255)
pdf.cell(15,5,"FCD".decode("UTF-8"),'LTBR',0,'C',1)
pdf.set_fill_color(255,255,255)
pdf.set_text_color(24,29,31)
pdf.cell(15,5,"0".decode("UTF-8"),'LTBR',0,'C',1)
pdf.set_fill_color(97,97,97)
pdf.set_text_color(255,255,255)
pdf.cell(15,5,"PCC".decode("UTF-8"),'LTBR',0,'C',1)
pdf.set_fill_color(255,255,255)
pdf.set_text_color(24,29,31)
pdf.cell(15,5,"0".decode("UTF-8"),'LTBR',0,'C',1)
pdf.set_fill_color(97,97,97)
pdf.set_text_color(255,255,255)
pdf.cell(15,5,"TOTAL".decode("UTF-8"),'LTBR',0,'C',1)
pdf.set_fill_color(255,255,255)
pdf.set_text_color(24,29,31)
pdf.cell(15,5,"30000000".decode("UTF-8"),'LTBR',0,'C',1)
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

pdf.set_auto_page_break(1,50)

pdf.output('estadisticas_ubch.pdf','F')
