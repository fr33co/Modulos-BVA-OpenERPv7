# -*- coding: utf-8 -*-

import time #Necesario para las funciones de Fecha
from datetime import date
from openerp.osv import osv, fields

class NominaBecadoIndividual(osv.Model):
	_name="becados.nominaindividual"

	_order = 'codigo'
	
	_rec_name = 'codigo'
	
	_columns = {
		'nomina' : fields.many2one("becados.nomina", "Nómina", required=False),
		'codigo' : fields.char(string="Código de la nómina", size=20, required=False),
		'becado': fields.many2one("hr.employee", "Becado", required = True, domain=[('categoria','=','1'),('status','=','1')]),
		'anyo' : fields.char(string="Año",required=True),
		'mes' : fields.selection((('Enero','Enero'),('Febrero','Febrero'),('Marzo','Marzo'),('Abril','Abril'),('Mayo','Mayo'),('Junio','Junio'),('Julio','Julio'),('Agosto','Agosto'),('Septiembre','Septiembre'),('Octubre','Octubre'),('Noviembre','Noviembre'),('Diciembre','Diciembre')),"Mes",required=True),
		'tipo_beca' : fields.many2one("becados.tipobeca", "Tipo de Beca", required=True),
		'asignacion' : fields.float(string="Asignación", required=True) 
	}
	
	_defaults = {
		'anyo' : lambda *a: time.strftime("%Y"),
	}
