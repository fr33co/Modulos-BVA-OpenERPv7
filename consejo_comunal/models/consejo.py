# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class Consejo(osv.Model):
	_name = "consejocomunal.consejo"
	
	_columns = {
		#Inicio de la seccion I (Identificacion Geografica)
		'fecha_r' : fields.date(string="Fecha de Realización", required=True),
		'nombre_emp' : fields.char(string="Nombre del Empadronador", size=25, required=True),
		'municipio' : fields.selection((('1','Girardot'),('2','Libertador')),"Municipio", required=True),
		'parroquia' : fields.selection((('1','Pedro José Ovalles'),('2','Palo Negro')),"Parroquia", required=True),
		'localidad' : fields.char(string="Localidad", size=100, required=True, select=1),
		'direccion' : fields.char(string="Dirección", size=256, required=True),
		#Inicio de la Seccion II (Area Organizativa del Consejo Comunal)
		'nombre_consejo' : fields.char(string="Nombre del Consejo Comunal", size=50, required=True),
		'legalizacion' : fields.selection((('1','SÍ'),('0','NO')),"Consejo Comunal Legalizado", required=True),
		'numero_reg' : fields.integer(string="Número de registro del Consejo", required=True),
		'conformacion' : fields.selection((('1','SÍ'),('0','NO')),"Consejo Comunal Conformado", required=True),
		'conformacion_proceso' : fields.selection((('1','SÍ'),('0','NO')),"Consejo Comunal en Proceso de Conformación", required=True),
		'vocerias_vencidas' : fields.selection((('1','SÍ'),('0','NO')),"Consejo Comunal con vocerias vencidas", required=True),
		'vocerias_vigentes' : fields.selection((('1','SÍ'),('0','NO')),"Consejo Comunal con vocerias vigentes", required=True),
		'origen' : fields.selection((('1','Indígena'),('2','Rural'),('3','Urbana')),"Origen del Consejo Comunal", required=True),
		'integracion_batalla' : fields.selection((('1','SÍ'),('0','NO')),"Integración a sala de Batalla Social", required=True),
		'comuna_construccion' : fields.selection((('1','SÍ'),('0','NO')),"¿Pertenece a Comuna en Construcción?", required=True),
		'reforma_consejos' : fields.selection((('1','Todas las personas'),('2','Algunas de las personas'),('3','Pocas personas'),('4','Ninguna de las personas')),"Conocimiento de Reforma de Consejos", required=True),
		#Inicio de la seccion III (Caracteristicas Demograficas)
		'cantidad_hab' : fields.integer(string="Cantidad de habitantes en el ámbito geográfico",required=True),
		'num_hombres' : fields.integer(string="Número de hombres", required=True),
		'num_mujeres' : fields.integer(string="Número de mujeres", required=True),
		'num_familias' : fields.integer(string="Número de familias", required=True),
		'num_viviendas' : fields.integer(string="Número de viviendas", required=True),
		'num_ninos' : fields.integer(string="¿Cuántos niños?", required=True),
		'num_ninas' : fields.integer(string="¿Cuántas niñas?", required=True),
		'num_adolescentes' : fields.integer(string="¿Cuántos adolescentes?", required=True),
		'num_adultos' : fields.integer(string="¿Cuántos adultos?", required=True),
		'num_adultos_mayores' : fields.integer(string="Número de adultos mayores de 60 años", required=True),
		'num_pers_discapacidad' : fields.integer(string="Número de personas con discapacidad permanente", required=True),
		'madres_solteras' : fields.selection((('1','SÍ'),('0','NO')),"Madres solteras como única fuente de sustento familiar", required=True),
		'num_madres_solteras' :fields.integer(string="Número de madres solteras como único sustento familiar",required=True),
		'num_madres_solteras_des' : fields.integer(string="¿Cuántas de esas madres solteras están desocupadas?", required=True),
		#Inicio de la seccion IV (Area Organizativa del Consejo Comunal)
		'alma_mater' : fields.boolean(string="Alma Mater"),
		'ribas' : fields.boolean(string="Ribas"),
		'robinson' : fields.boolean(string="Robinson"),
		'robinsonII' : fields.boolean(string="RobinsonII"),
		'robinsonIII' : fields.boolean(string="RobinsonIII"),
		'sucre' : fields.boolean(string="Sucre"),
		'escuelas_bolivarianas' : fields.selection((('1','SÍ'),('0','NO')),"Escuelas Bolivarianas",required=True),
		'escuelas_bol_ope' : fields.boolean(string="Operativo"),
		'simoncito' : fields.selection((('1','SÍ'),('0','NO')),"Simoncito",required=True),
		'simoncito_ope' : fields.boolean(string="Operativo"),
		'escuelas_oficiales' : fields.selection((('1','SÍ'),('0','NO')),"Escuelas Oficiales",required=True),
		'escuelas_ofi_ope' : fields.boolean(string="Operativo"),
		'aldeas_univeritarias' : fields.selection((('1','SÍ'),('0','NO')),"Aldeas Universitarias",required=True),
		'aldeas_uni_ope' : fields.boolean(string="Operativo"),
		'universidad_estatal' : fields.selection((('1','SÍ'),('0','NO')),"Universidad del Estado",required=True),
		'universidad_est_ope' : fields.boolean(string="Operativo"),
		'universidad_privada' : fields.selection((('1','SÍ'),('0','NO')),"Universidad Privada",required=True),
		'universidad_pri_ope' : fields.boolean(string="Operativo"),
		'nucleos_universitario' : fields.selection((('1','SÍ'),('0','NO')),"Núcleos Universitarios",required=True),
		'nucleos_uni_ope' : fields.boolean(string="Operativo"),
		'escuelas_robinson' : fields.selection((('1','SÍ'),('0','NO')),"Escuelas Robinsonianas",required=True),
		'escuelas_robin_ope' : fields.boolean(string="Operativo"),
		'inces' : fields.selection((('1','SÍ'),('0','NO')),"INCES",required=True),
		'inces_ope': fields.boolean(string="Operativo"),
	}