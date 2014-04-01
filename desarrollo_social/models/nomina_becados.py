# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import fields, osv
import base64#Necesario para la generación del .txt
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring#Necesario para la generación del .xsl

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
			stage = x_browse_id.stage_id #Leer el estado de la nómina actual
			print "Id de la pre-nómina: "+str(id_nomina)+"\n"
			print "mes de la pre-nómina: "+str(mes)+"\n"
			print "Stage de la pre-nómina: "+str(stage)+"\n"
			
			#~ cedula = ""
			#~ name = ""
			#~ tipo_beca = ""
			for becado in x_browse_id.becados:#Recorrer los registros dentro del campo 'becados' del modelo de Nómina
				print str(becado.cedula)+" "+str(becado.name_related.encode("utf-8"))+" "+str(becado.tipo_beca.tipo_beca.encode("utf-8"))
				#~ cedula = cedula + str(becado.cedula)
				#~ name = name + str(becado.name_related.encode("utf-8"))
				#~ tipo_beca = tipo_beca + str(becado.tipo_beca.tipo_beca.encode("utf-8"))
				codigo = str(mes)+str(anyo)+str(becado.cedula)
				tipo_beca = becado.tipo_beca.id
				id_att = obj_proceso_nomina.create(cr, uid, {
					'nomina': id_nomina, 
					'codigo': codigo,
					'becado': becado.id,
					'anyo': anyo,
					'mes': mes,
					'tipo_beca': tipo_beca,
					'asignacion': 0,
					}, context=context)
	
		
	#Función para la generación de los reportes .txt y xsl de la pre-nómina----------------------------------------------------------	
	def action_archivar_prenomina(self, cr, uid, ids, context):
		
		obj_proceso_nomina = self.pool.get('becados.nomina')#Selección del modelo a consultar
		browse_id = self.browse(cr, uid, ids, context=None)#Arreglo de los campos del modelo (objeto) actual
		for x_browse_id in browse_id:#Recorrer el arreglo para seleccionar el campo necesario
			id_nomina = x_browse_id.id #Leer el identificaddor de la nómina actual
			mes = x_browse_id.mes #Leer el mes de la nómina actual
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
						for becado in nomina.becados:
							datos = str(becado.cedula)+" "+str(becado.name_related.encode("utf-8"))+" "+str(becado.status)+"\n"
							#~ llenar_archivo = open(nombre_archivo,'a')
							#~ llenar_archivo.write(datos)							
							#~ llenar_archivo.close()
							data = data + datos
						print data
					id_att = self.registro_archivo(cr, uid, id_nomina, mes, data, stage, context)
			
			else:
				print "No se encontró ningún registro"
				
		
	#Función para la generación de los reportes .txt y xsl de la nómina--------------------------------------------------------------	
	def action_archivar_nomina(self, cr, uid, ids, context):
		
		obj_proceso_nomina = self.pool.get('becados.nomina')#Selección del modelo a consultar
		browse_id = self.browse(cr, uid, ids, context=None)#Arreglo de los campos del modelo (objeto) actual
		for x_browse_id in browse_id:#Recorrer el arreglo para seleccionar el campo necesario
			id_nomina = x_browse_id.id #Leer el identificaddor de la nómina actual
			mes = x_browse_id.mes #Leer el mes de la nómina actual
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
						for becado in nomina.becados:
							datos = str(becado.cedula)+" "+str(becado.name_related.encode("utf-8"))+" "+str(becado.status)+"\n"
							data = data + datos
						print data
					id_att = self.registro_archivo(cr, uid, id_nomina, mes, data, stage, context)
					
			else:
				print "No se encontró ningún registro"
				
					
	#Función para la generación de los reportes .txt y xsl del cierre de nómina------------------------------------------------------
	def action_archivar_cierre(self, cr, uid, ids, context):
		
		obj_proceso_nomina = self.pool.get('becados.nomina')#Selección del modelo a consultar
		browse_id = self.browse(cr, uid, ids, context=None)#Arreglo de los campos del modelo (objeto) actual
		for x_browse_id in browse_id:#Recorrer el arreglo para seleccionar el campo necesario
			id_nomina = x_browse_id.id #Leer el identificaddor de la nómina actual
			mes = x_browse_id.mes #Leer el mes de la nómina actual
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
						for becado in nomina.becados:
							datos = str(becado.cedula)+" "+str(becado.name_related.encode("utf-8"))+" "+str(becado.status)+"\n"
							data = data + datos
						print data
					id_att = self.registro_archivo(cr, uid, id_nomina, mes, data, stage, context)
		
		else:
				print "No se encontró ningún registro"
				
				
	#Función para el registro de los archivos generados de la nómina-----------------------------------------------------------------
	def registro_archivo(self, cr, uid, nomina, mes, data, stage, context):
		#Registro del .txt					
		#~ fecha = time.strftime('%d%m%y')
		print data
		dia = time.strftime('%d')
		anyo = time.strftime('%Y')
		fecha = dia+"-"+mes+"-"+anyo
		nombre_archivo = str(stage)+ "-" + fecha +'.'+ 'txt'
		id_att = self.pool.get('ir.attachment').create(cr, uid, {
			'nomina': nomina, 
			'name': nombre_archivo,
			'res_name': nombre_archivo,
			'datas': base64.encodestring(data),
			'datas_fname': nombre_archivo,
			'res_model': 'becados.nomina',
			}, context=context)
		return id_att
		
		
	_columns = {
		'anyo' : fields.char(string="Año",required=True),
		'mes' : fields.selection((('Enero','Enero'),('Febrero','Febrero'),('Marzo','Marzo'),('Abril','Abril'),('Mayo','Mayo'),('Junio','Junio'),('Julio','Julio'),('Agosto','Agosto'),('Septiembre','Septiembre'),('Octubre','Octubre'),('Noviembre','Noviembre'),('Diciembre','Diciembre')),"Mes",required=True),
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
		#~ 'status' : '1',
	}

