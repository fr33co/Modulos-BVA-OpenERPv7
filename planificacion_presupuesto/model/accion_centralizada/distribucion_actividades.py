# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class distribucion_actividades(osv.Model):

	_name = "distribucion.actividades"

	_columns = {
		'distribucion_ids':fields.many2one('accion.centralizada', 'distribucion_actividades', ondelete='cascade', select=False),
		'actividades' : fields.char(string="Actividades", size=60, required=False),
		'unidad_medida' : fields.char(string="Unidad de Medida", size=35, required=False),
		'cantidad' : fields.integer(string="Cantidad", required=False),
		'medio_verifi' : fields.char(string="Medio de Verificación", size=40, required=False),
		'indicadores_act' : fields.char(string="Indicadores de la Actividad", size=50, required=False),

	}