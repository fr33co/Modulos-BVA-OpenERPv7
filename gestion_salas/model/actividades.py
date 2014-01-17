from openerp.osv import osv, fields

#Clase Informacion opcional
class registrar_actividades(osv.Model):

	_name = "actividades"
	_order = 'motivo'
	_rec_name = 'motivo'
	_columns = {
		'motivo' : fields.char(string="Actividad", size=35),
	}