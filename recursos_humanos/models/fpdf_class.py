# -*- coding: utf-8 -*-
from fpdf import FPDF
import fpdf
#####################################################################################################
#				CLASE CONSTRUCTORA PDF SLIP
#####################################################################################################
class Nomina_slip(FPDF):

	def header(self):
		#Arial bold 15
		self.set_font('Arial','B',15)
		
		self.image('openerp/addons/recursos_humanos/img/gob.jpg',20,10,50) # Imagen Superior
		
		self.image('openerp/addons/recursos_humanos/img/logo_bva2.jpg',210,15,50) # Imagen Indferior
		
		self.set_draw_color(0,80,180)
		self.set_fill_color(28,108,198)
		self.set_text_color(220,50,50)
		self.ln(10)

	# Page footer
	def footer(self):
		#Posición a 1.5 cm desde abajo
		self.set_y(-15)
		#Arial italic 8
		self.set_font('Arial','I',8)
		#Color de texto en gris
		self.set_text_color(128)
		#Numero de paginas
		self.cell(0,10,'Pagina '+str(self.page_no())+"/"+str(self.alias_nb_pages()),0,0,'R')

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

	def print_chapter(self,num,title,name):
		self.add_page()
		self.chapter_title(num,title)
		self.chapter_body(name)
#####################################################################################################
class Constancia(FPDF):
	
	def header(self):
		#Arial bold 15
		self.set_font('Arial','B',15)
		
		# ALINEACION DE LA IMAGEN EN LA CABECERA DEL DOCUMENTO
		# (CAMPO 1 = HORIZONTAL , CAMPO 2 = VERTICAL, CAMPO 3 = DIMENCION DE LA IMAGEN)
		
		self.image('openerp/addons/recursos_humanos/img/gob.jpg',10,10,50) # IMAGEN SUPERIOR
		self.image('openerp/addons/recursos_humanos/img/logo_bva2.jpg',150,15,50) # IMAGEN INFERIOR
		self.image('openerp/addons/recursos_humanos/img/img_bot.jpg',15,245,190) # IMAGEN INFERIOR
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
		self.ln(20)

		
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
		#self.cell(0,10,'Pagina '+str(self.page_no()),0,0,'R') 
		
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
		
########################################################################################################

class Alimentacion(FPDF):
	
	def header(self):
		#Arial bold 15
		self.set_font('Arial','B',15)
		# ALINEACION DE LA IMAGEN EN LA CABECERA DEL DOCUMENTO
		# (CAMPO 1 = HORIZONTAL , CAMPO 2 = VERTICAL, CAMPO 3 = DIMENCION DE LA IMAGEN)
		
		#~ self.image('logo_bva.jpg',15,-0,150)
		
		self.image('openerp/addons/recursos_humanos/img/gob.jpg',15,10,50) # Imagen Superior
		
		self.image('openerp/addons/recursos_humanos/img/logo_bva2.jpg',209,15,50) # Imagen Indferior
		
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
		self.ln(30)

		
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
		
		self.cell(0,10,'Pagina '+str(self.page_no())+"/"+str(self.alias_nb_pages()),0,0,'R')
		
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
		
######################################################################
class Bono(FPDF):
	
	def header(self):
		#Arial bold 15
		self.set_font('Arial','B',15)
		
		# ALINEACION DE LA IMAGEN EN LA CABECERA DEL DOCUMENTO
		# (CAMPO 1 = HORIZONTAL , CAMPO 2 = VERTICAL, CAMPO 3 = DIMENCION DE LA IMAGEN)
		
		self.image('openerp/addons/recursos_humanos/img/gob.jpg',20,10,35)
		self.image('openerp/addons/recursos_humanos/img/logo_bva2.jpg',165,13,35)
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
		self.ln(20)

		
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


# METODOS GLOBALES
######################################################################
def acento(cadena):
	result = cadena.encode('UTF-8').decode('UTF-8') # INSTITUCION
	return result
#####################################################################
# Metodo global para fechas
def fecha(fecha):
	date = fecha.split("-")
	nueva_fecha = date[2]+"/"+date[1]+"/"+date[0]
	return nueva_fecha
#####################################################################
# Metodo global para redondear
def decimal(cadena):
	salida = "%.2f" % round(cadena,2)
	return salida
#####################################################################
# METODO GLOBAL PARA EL
#####################################################################
def resolve_o2m_operations(cr, uid, target_osv, operations, fields, context):
    results = []
    for operation in operations:
        result = None
        if not isinstance(operation, (list, tuple)):
            result = target_osv.read(cr, uid, operation, fields, context=context)
        elif operation[0] == 0:
            # may be necessary to check if all the fields are here and get the default values?
            result = operation[2]
        elif operation[0] == 1:
            result = target_osv.read(cr, uid, operation[1], fields, context=context)
            if not result: result = {}
            result.update(operation[2])
        elif operation[0] == 4:
            result = target_osv.read(cr, uid, operation[1], fields, context=context)
        if result != None:
            results.append(result)
    return results
######################################################################
# PROCESO DE PUNTO DECIMAL, PARA LA CONVERSION DE CIFRAS, METODO GLOBAL
def punto_decimal(snum):
    "Adicionar comas como separadores de miles a n. n debe ser de tipo string"
    s = snum;
    i = s.index('.') # Se busca la posición del punto decimal
    while i > 3:
        i = i - 3
        s = s[:i] +  '#' + s[i:]
	
    n = s.replace(".", ",", 5);
    t = n.replace("#", ".", 5);
    return t
#######################################################################
