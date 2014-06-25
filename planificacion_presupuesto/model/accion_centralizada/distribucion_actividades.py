# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class distribucion_actividades(osv.Model):

	_name = "distribucion.actividades"

	_columns = {
		'distribucion_ids':fields.many2one('accion.centralizada', 'distribucion_actividades', ondelete='cascade', select=False),
		'actividades' : fields.char(string="Actividades", required=False),
		'unidad_medida' : fields.char(string="Unidad de Medida", required=False),
		'cantidad' : fields.integer(string="Cantidad", required=False),
		'medio_verifi' : fields.char(string="Medio de Verificación", required=False),
		'indicadores_act' : fields.char(string="Indicadores de la Actividad", required=False),

	}