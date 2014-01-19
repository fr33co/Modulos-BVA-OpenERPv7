# -*- coding: utf-8 -*-
{
	'name' : "Solicitud y Soporte Técnico de Canaimitas",
	'category' : "Others",
	'version' :  "1.0",
	'depends' : ['base', 'l10n_ve_topology'],
	'autor' : "Marcel Arcuri, Angel Guadarrama & A.C. Bibliotecas Virtuales de Aragua", 
	'description' : """\
		Modulo para la gestión de las solicitudes y soporte técnico para Canaimitas""",
	'data': [
		'view/solicitud_soporte.xml',
		'view/solicitud_reparacion.xml',
		'security/groups.xml',
		'security/ir.model.access.csv',
	],		
}
