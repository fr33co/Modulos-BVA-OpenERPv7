# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import fields, osv
import base64#Necesario para la generación del .txt
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring#Necesario para la generación del .xsl
from fpdf import FPDF
import fpdf
import pdf_nominas

class NominaBecados(osv.Model):
	
	_name = 'becados.nomina'
	
	#Función para pasar a estado de Pre-nómina----------------------------------------------
	def action_prenomina(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'stage_id':'prenomina'}, context=context)
		
	#Función para pasar a estado de Nómina-------------------------------------------------------------------------------------------
	def action_nomina(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'stage_id':'nomina'}, context=context)
		
	#Función para pasar a estado de Cierre de Nómina---------------------------------------------------------------------------------
	def action_cierre(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'stage_id':'cierre'}, context=context)
		
	#Función para pasar a estado de Cancelado----------------------------------------------------------------------------------------
	def action_cancelar(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'stage_id':'cancelado'}, context=context)
	
	
	#Función para pasar a estado de Cancelado----------------------------------------------------------------------------------------
	def generar_nominas(self, cr, uid, ids, context=None):
		
		obj_proceso_nomina = self.pool.get('becados.nominaindividual')#Selección del modelo a consultar
		browse_id = self.browse(cr, uid, ids, context=None)#Arreglo de los campos del modelo (objeto) actual
		for x_browse_id in browse_id:#Recorrer el arreglo para seleccionar los campos necesarios
			id_nomina = x_browse_id.id #Leer el identificaddor de la nómina actual
			anyo = x_browse_id.anyo
			mes = x_browse_id.mes #Leer el mes de la nómina actual
			tiponomina = x_browse_id.tipo_nomina #Leer el tipo de nómina de la nómina actual
			stage = x_browse_id.stage_id #Leer el estado de la nómina actual
			print "Id de la pre-nómina: "+str(id_nomina)+"\n"
			print "mes de la pre-nómina: "+str(mes)+"\n"
			print "Stage de la pre-nómina: "+str(stage)+"\n"
			
			for becado in x_browse_id.becados:#Recorrer los registros dentro del campo 'becados' del modelo de Nómina
				cedula = becado.cedula
				name = becado.name_related
				tipo_beca = becado.tipo_beca.id
				asignacion = becado.tipo_beca.asignacion
				
				print cedula + " " + name + " " + str(tipo_beca)
				
				#Preparación de los datos compuestos
				codigo = str(mes)+str(anyo)+str(cedula)
								
				#Verificamos si la nómina individual del becado ya fue generada (se toma en cuenta el código)
				search_nomina1 = obj_proceso_nomina.search(cr, uid, [('codigo','=',codigo)], count=False)
				
				if not search_nomina1: #Verificar esto, al parecer impide que se listen algunas nóminas individuales 
				
					id_att = obj_proceso_nomina.create(cr, uid, {
						'nomina': id_nomina, 
						'codigo': codigo,
						'becado': becado.id,
						'anyo': anyo,
						'mes': mes,
						'tipo_beca': tipo_beca,
						'asignacion': asignacion,
						}, context=context)
				
				else:
					print "La nómina ya existe..."
			
			print "\n"
			#Ahora verificamos si las nóminas individuales se corresponden con la lista de becados seleccionados.
			#Si alguna de éllas no pertenece a ningún becado de la lista, procedemos a eliminarla de la lista de nóminas
			for nomina in x_browse_id.nomina_individual:
				print nomina.codigo	+ " " + nomina.becado.cedula
				contador = 0 #Contador para validar si la nómina pertenece a algún becado seleccionado
				for becado2 in x_browse_id.becados:
					print ""+becado2.cedula
					if becado2.cedula == nomina.becado.cedula:
						print becado2.cedula+"=="+nomina.becado.cedula
						contador = contador + 1
					else:
						contador = contador 
				print contador
				print nomina.id
				
				if contador <= 0:
					obj_proceso_nomina.unlink(cr, uid, nomina.id, context=None)
					# Revisar: Hasta los momentos se actualiza la lista de nóminas individuales según el número de becados, 
					#pero ocurre un error si no se ha guardado la nómina después de borrar un becado de la lista y se intenta generar de nuevo la nómina.


	#Función para la generación de los reportes .txt y xsl de la pre-nómina----------------------------------------------------------	
	def action_archivar_prenomina(self, cr, uid, ids, context):
		
		obj_proceso_nomina = self.pool.get('becados.nomina')#Selección del modelo a consultar
		browse_id = self.browse(cr, uid, ids, context=None)#Arreglo de los campos del modelo (objeto) actual
		for x_browse_id in browse_id:#Recorrer el arreglo para seleccionar el campo necesario
			id_nomina = x_browse_id.id #Leer el identificaddor de la nómina actual
			mes = x_browse_id.mes #Leer el mes de la nómina actual
			tiponomina = x_browse_id.tipo_nomina.tipo_nomina #Leer el tipo de nómina de la nómina actual
			stage = x_browse_id.stage_id #Leer el estado de la nómina actual 
			print "Id de la nómina: "+str(id_nomina)+"\n"
			print "mes de la nómina: "+str(mes)+"\n"
			print "Stage de la nómina: "+str(stage)+"\n"
			#Ejecuto una consulta que retorne sólo el número de registros coincidentes
			search_nomina1 = obj_proceso_nomina.search(cr, uid, [('id','=',id_nomina)], count=True)
		
			if search_nomina1 > 0:
				print str(search_nomina1)+"\n"
				
				#Preparación del archivo txt (Forma alternativa)
				#~ dia = time.strftime('%d')
				#~ anyo = time.strftime('%Y')
				#~ fecha = dia+"-"+mes+"-"+anyo
				#~ nombre_archivo = stage+ "-" + fecha +'.'+ 'xls'
				#~ print nombre_archivo
				#~ archivo = open(nombre_archivo,'w')
				#~ if archivo:
					#~ archivo.close()
					#~ print "archivo creado"
				#~ else:
					#~ print "No se pudo crear el archivo"
				
				#Consulto los datos de la nómina con el id específicado en 'id_nomina'
				search_nomina2 = obj_proceso_nomina.search(cr, uid, [('id','=',id_nomina)])
				
				#Leo los datos de los registros resultantes
				leer_nominas = obj_proceso_nomina.read(cr, uid, search_nomina2, context=context)
			
				if leer_nominas:
					#Recorro los campos de la nómina actual
					for nomina in self.browse(cr, uid, ids, context=None):
						#Recorro los registros que están dentro del campo 'becados' de la nómina actual
						data = ""
						data1 = []
						for becado in nomina.nomina_individual:
							datos = str(becado.codigo)+" "+str(becado.becado.cedula)+" "+str(becado.becado.name_related.encode("utf-8"))+" "+str(becado.becado.status)+" "+str(becado.tipo_beca.id)+" "+str(becado.asignacion)+"\n"
							datos1 = []
							datos1.append(str(becado.codigo))
							datos1.append(str(becado.becado.cedula))
							datos1.append(str(becado.becado.name_related.encode("utf-8")))
							datos1.append(str(becado.becado.status))
							datos1.append(str(becado.tipo_beca.id))
							datos1.append(str(becado.asignacion))
							#~ llenar_archivo = open(nombre_archivo,'a')
							#~ llenar_archivo.write(datos)							
							#~ llenar_archivo.close()
							data = data + datos
							data1.append(datos1)
							
						print data
						print datos1
						
						
					#Ejecutamos el método de registro del txt 
					id_att = self.registro_archivo(cr, uid, id_nomina, tiponomina, mes, data, stage, context)
					
					#Ejecutamos el método de generación de reportes en PDF
					gen_pdf = self.generar_pdf(data1)
			
			else:
				print "No se encontró ningún registro"
				
		
	#Función para la generación de los reportes .txt y xsl de la nómina--------------------------------------------------------------	
	def action_archivar_nomina(self, cr, uid, ids, context):
		
		obj_proceso_nomina = self.pool.get('becados.nomina')#Selección del modelo a consultar
		browse_id = self.browse(cr, uid, ids, context=None)#Arreglo de los campos del modelo (objeto) actual
		for x_browse_id in browse_id:#Recorrer el arreglo para seleccionar el campo necesario
			id_nomina = x_browse_id.id #Leer el identificaddor de la nómina actual
			mes = x_browse_id.mes #Leer el mes de la nómina actual
			tiponomina = x_browse_id.tipo_nomina.tipo_nomina #Leer el tipo de nómina de la nómina actual
			stage = x_browse_id.stage_id #Leer el estado de la nómina actual
			print "Id de la pre-nómina: "+str(id_nomina)+"\n"
			print "mes de la pre-nómina: "+str(mes)+"\n"
			print "Stage de la pre-nómina: "+str(stage)+"\n"
			#Ejecuto una consulta que retorne sólo el número de registros coincidentes
			search_nomina1 = obj_proceso_nomina.search(cr, uid, [('id','=',id_nomina)], count=True)
			
			if search_nomina1 > 0:
				print str(search_nomina1)+"\n"
				
				#Consulto los datos de la nómina con el id específicado en 'id_nomina'
				search_nomina2 = obj_proceso_nomina.search(cr, uid, [('id','=',id_nomina)])
				
				#Leo los datos de los registros resultantes
				leer_nominas = obj_proceso_nomina.read(cr, uid, search_nomina2, context=context)
			
				if leer_nominas:
					#Recorro los campos de la nómina actual
					for nomina in self.browse(cr, uid, ids, context=None):
						#Recorro los registros que están dentro del campo 'becados' de la nómina actual
						data = ""
						for becado in nomina.nomina_individual:
							datos = str(becado.codigo)+" "+str(becado.becado.cedula)+" "+str(becado.becado.name_related.encode("utf-8"))+" "+str(becado.becado.status)+" "+str(becado.tipo_beca.id)+" "+str(becado.asignacion)+"\n"
							data = data + datos
						print data
					id_att = self.registro_archivo(cr, uid, id_nomina, tiponomina, mes, data, stage, context)
					
			else:
				print "No se encontró ningún registro"
				
					
	#Función para la generación de los reportes .txt y xsl del cierre de nómina------------------------------------------------------
	def action_archivar_cierre(self, cr, uid, ids, context):
		
		obj_proceso_nomina = self.pool.get('becados.nomina')#Selección del modelo a consultar
		browse_id = self.browse(cr, uid, ids, context=None)#Arreglo de los campos del modelo (objeto) actual
		for x_browse_id in browse_id:#Recorrer el arreglo para seleccionar el campo necesario
			id_nomina = x_browse_id.id #Leer el identificaddor de la nómina actual
			mes = x_browse_id.mes #Leer el mes de la nómina actual
			tiponomina = x_browse_id.tipo_nomina.tipo_nomina #Leer el tipo de nómina de la nómina actual
			stage = x_browse_id.stage_id #Leer el estado de la nómina actual
			print "Id de la pre-nómina: "+str(id_nomina)+"\n"
			print "mes de la pre-nómina: "+str(mes)+"\n"
			print "Stage de la pre-nómina: "+str(stage)+"\n"
			#Ejecuto una consulta que retorne sólo el número de registros coincidentes
			search_nomina1 = obj_proceso_nomina.search(cr, uid, [('id','=',id_nomina)], count=True)
			
			if search_nomina1 > 0:
				print str(search_nomina1)+"\n"
				
				#Consulto los datos de la nómina con el id específicado en 'id_nomina'
				search_nomina2 = obj_proceso_nomina.search(cr, uid, [('id','=',id_nomina)])
				
				#Leo los datos de los registros resultantes
				leer_nominas = obj_proceso_nomina.read(cr, uid, search_nomina2, context=context)
			
				if leer_nominas:
					#Recorro los campos de la nómina actual
					for nomina in self.browse(cr, uid, ids, context=None):
						#Recorro los registros que están dentro del campo 'becados' de la nómina actual
						data = ""
						for becado in nomina.nomina_individual:
							datos = str(becado.codigo)+" "+str(becado.becado.cedula)+" "+str(becado.becado.name_related.encode("utf-8"))+" "+str(becado.becado.status)+" "+str(becado.tipo_beca.id)+" "+str(becado.asignacion)+"\n"
							data = data + datos
						print data
					id_att = self.registro_archivo(cr, uid, id_nomina, tiponomina, mes, data, stage, context)
		
		else:
				print "No se encontró ningún registro"
				
				
	#Función para el registro de los archivos generados de la nómina-----------------------------------------------------------------
	def registro_archivo(self, cr, uid, nomina, tipo_nomina, mes, data, stage, context):
		#Registro del .txt					
		#~ fecha = time.strftime('%d%m%y')
		print data
		#~ dia = time.strftime('%d')
		anyo = time.strftime('%Y')
		fecha = mes+"-"+anyo
		nombre_archivo = str(stage) + "-" + tipo_nomina + "-" + fecha +'.'+ 'txt'
		id_att = self.pool.get('ir.attachment').create(cr, uid, {
			'nomina': nomina, 
			'name': nombre_archivo,
			'res_name': nombre_archivo,
			'datas': base64.encodestring(data),
			'datas_fname': nombre_archivo,
			'res_model': 'becados.nomina',
			}, context=context)
		return id_att
		
		
	#Fucnión para la generación de reportes en PDF de la nómina
	def generar_pdf(self,data1):
		regs = len(data1)
		print "Cantidad de registros: "+str(regs)+"\n"
		print data1
		print "\n"
		for reg in data1:
			print reg
			print "\n"
			
		pdf = FPDF(orientation='L',unit='mm',format='letter') #Da error si intento llamar a la clase PDF() importada desde pdf_nominas en vez de FPDF()
		pdf.add_page()
		pdf.set_font('Arial','B',16)
		pdf.cell(15,10,'Codigo')
		pdf.cell(40,10,'Becado')
		pdf.cell(40,10,'Anyo')
		pdf.cell(40,10,'Mes')
		pdf.cell(40,10,'Tipo de Beca')
		pdf.cell(40,10,'Asignacion')
		pdf.ln()
		
		#~ i = 0
		
		for linea in data1:
			#~ print i
			#Probar con los datos que vienen en data1 y verificar por qué se muestra desde 'prueba2'
			pdf.cell(15,10,'prueba1')
			pdf.cell(40,10,'prueba2')
			pdf.cell(40,10,'prueba3')
			pdf.cell(40,10,'prueba4')
			pdf.cell(40,10,'prueba5')
			pdf.cell(40,10,'prueba6')
			pdf.ln()

			#~ i = i +1
		 
		pdf.output('openerp/addons/desarrollo_social/reportes/nominas/tuto1.pdf','F')		 

		print "<script>document.location = 'openerp/addons/desarrollo_social/reportes/nominas/tuto1.pdf';</script>"		
		
	_columns = {
		'anyo' : fields.char(string="Año",required=True),
		'mes' : fields.selection((('Enero','Enero'),('Febrero','Febrero'),('Marzo','Marzo'),('Abril','Abril'),('Mayo','Mayo'),('Junio','Junio'),('Julio','Julio'),('Agosto','Agosto'),('Septiembre','Septiembre'),('Octubre','Octubre'),('Noviembre','Noviembre'),('Diciembre','Diciembre')),"Mes",required=True),
		'tipo_nomina' : fields.many2one('becados.tiponomina','Tipo de Nómina',required=True),
		#~ 'status' : fields.selection((('1','Activo'),('2','Periódo de gracia'),('3','Permiso de reposo'),('4','Permiso no remunerado'),('5','Suspendido'),('6','Vacaciones'),('7','Egresado')), "Estatus", required = False),
		#~ 'tipo_nomina' : fields.many2one("becados.tiponomina","Tipo de Nómina",required=False),
		#~ 'tipo_beca' : fields.many2one("becados.tipobeca","Tipo de Beca",required=False),
		#~ 'ejes' : fields.many2one("becados.ejes","Eje",required=False),
		#~ 'sedes' : fields.many2one("becados.sedes","Sede",required=False),
		'becados' : fields.many2many("hr.employee","proceso_nomina","becados_nomina_id","hr_employee_id","Becados",required=True, domain=[('categoria','=','1'),('status','=','1')]),
		'nomina_individual' : fields.one2many("becados.nominaindividual", "nomina", string="Nóminas", required=False),
		'archivos' : fields.one2many("ir.attachment", "nomina", string="Archivos de nómina", required="False"),
		#Podemos ver que el campo de 'becados', de tipo many2many, contiene 5 parametros:
		#"hr.employee", indica el nombre del modelo al que se va a hacer relación (modelo de empleados).
		#"proceso_nomina", indica el nombre del modelo que se creará para ser intermediario entre el modelo actual (modelo de nomina) y el modelo a relacionar (modelo de empleados).
		#"becados_nomina_id", indica un nombre de id que representará al modelo actual (modelo de nomina) en el modelo intermediario.
		#"hr_employee_id", indica un nombre de id que representará al modelo a relacionar (modelo de empleados) en el modelo intermediario.
		'stage_id' : fields.selection((('prenomina','Pre-nómina'),('nomina','Nómina'),('cierre','Cerrado'),('cancelado','Cancelado')), "Estado", required=True),
	}
	
	_defaults = {
		'stage_id' : 'prenomina',
		'anyo' : lambda *a: time.strftime("%Y"),
		'tipo_nomina' : '1'
		#~ 'status' : '1',
	}

