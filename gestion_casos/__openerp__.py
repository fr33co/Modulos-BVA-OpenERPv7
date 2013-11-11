{ # Archivo descriptivo Configuracion OpenERP
    'name' : "Monitor de Casos",
    'category' : "Registro de Casos",
    'version' : "1.0",
    'depends' : ['base'],
    'author' : "Ing Jesus Laya",
    'description' : """\
	Modulo para la Gestión de Casos:
    - Caso Alumbrado
    - Caso Vialidad
    - Caso Salud
    - Caso Vivienda
    - Caso Aseo
    - Caso Educación
    - Registro de Casos""",
    'data' : [
			'view/casos.xml', #Declaracion de la vista Monitor de Casos
			#'view/partner.xml',
			],
}
