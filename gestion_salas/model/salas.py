import random
from openerp.osv import osv, fields


class registrar_salas(osv.Model):
	_name = "registrar"
	_order = 'sala_nombre'
	_rec_name = 'sala_nombre'
	_columns = {
	'c_sala' : fields.char(string="Codigo de la Sala", size=8, readonly=False, required=True),
	'sala_nombre' : fields.char(string="Nombre de la Sala", size=35, required=True),
	'sede' : fields.many2one('sedes2', 'Sede'),
	'estado' : fields.char(string="Estado", size=25),
	'ciudad' : fields.char(string="Ciudad", size=25),
	'municipio' : fields.char(string="Municipio", size=25),
	'parroquia' : fields.char(string="Parroquia", size=25),
	'sector' : fields.char(string="Sector", size=25),
	'direccion' : fields.char(string="Direccion", size=100, required=True),
	'observaciones' : fields.char(string="Observaciones"),		
	}

	def _get_last_id(self, cr, uid, ids, context = None):

                sfl_id       = self.pool.get('registrar')
                srch_id      = sfl_id.search(cr,uid,[])
                rd_id        = sfl_id.read(cr, uid, srch_id, context=context)
                if rd_id:
                    id_documento = rd_id[-1]['c_sala']
                    c_sala = id_documento[2:]
                    last_id      = c_sala.lstrip('0')
                    str_number   = str(int(last_id) + 1)
                    last_id      = str_number.rjust(5,'0')
                    codigo      = 'CS'+last_id
                else :
                    str_number = '1'
                    last_id      = str_number.rjust(5,'0')
                    codigo      = 'CS'+last_id
                return codigo

	_defaults = {
        'c_sala' : _get_last_id
    }

	def on_change_direccion(self, cr, uid, ids, sede, context=None):

		values = {}
		if not sede:
			return values
		direccion = self.pool.get('sedes2').browse(cr, uid, sede, context=context)
		values.update({
			'estado' : direccion.estado,
			'ciudad' : direccion.ciudad,
			'municipio' : direccion.municipio,
			})
		return {'value' : values}