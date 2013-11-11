import time
from openerp.osv import osv, fields
from datetime import datetime, timedelta

#Clase solicitud de sala
class Solicitar_Sala(osv.Model):
	_name = "solicitar.sala"
	_order = 'c_solicitud'
	_rec_name = 'c_solicitud'
	_columns = {
		'nombre' : fields.char(string="Nombre", size=25, required=False),
		'apellido' : fields.char(string="Apellido", size=25, required=False),
		'cedula' : fields.char(string="Cedula", size=8, required=False),
		'c_solicitud' : fields.char(string="Codigo de Solicitud", size=8, readonly=False, required=False),
		'fh_inicio' : fields.datetime(string="Fecha/Hora Inicio", required=False),
		'motivo' : fields.selection((('1','Exposicion'), ('2','Reunion'), ('3', 'Cine Foro'), ('4','Charla'),('5','Presentacion de Tesis')),'Actvidad a realizar', required=False),
		'fh_final' : fields.datetime(string="Fecha/Hora Conclusion", required=False),
		'descripcion' : fields.text(string="Descripcion"),
		'telefono' : fields.char(string="Telefono Recidencia", size=11),
		'celular' : fields.char(string="Celular", size=11, required=False),
		#'salas': fields.char(string="Salas", size=25, required=False), 
		'salas':fields.many2one('registrar.salas', 'Salas',required=False),
		'f_solicitud': fields.datetime('Fecha de Solicitud', readonly=False,  required=False),
		'facebook' : fields.char(string="Facebook", size=35),
		'twitter' : fields.char(string="Twitter", size=35),
		'facebook' : fields.char(string="Facebook", size=35),
		'correo' : fields.char(string="Correo Electronico", size=35),
		'ciudad' : fields.char(string="Ciudad", size=25),
		'estado' : fields.char(string="Estado", size=25),
		'municipio' : fields.char(string="Municipio", size=25),
		'parroquia' : fields.char(string="Parroquia", size=25),
		'sector' : fields.char(string="Sector", size=25),


	}
	_defaults = {
        'c_solicitud': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'solicitar.sala'),
        'f_solicitud': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    } 

	def on_change_direccion(self, cr, uid, ids, salas, context=None):
	
	        values = {}
	        if not salas:
	            return values
	        direccion = self.pool.get('registrar.salas').browse(cr, uid, salas, context=context)
	        values.update({
	            'estado' : direccion.estado,
	            'ciudad' : direccion.ciudad,
	            'municipio' : direccion.municipio,
	        })
	        return {'value' : values}

	def onchange_inicio(self, cr, uid, ids, fh_inicio, context=None):
            """
            Onchange para validar que la fecha de inicio no es menor a la fecha de creacion
            """
            res = {}
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if fh_inicio < now:
                res['warning'] = {'title': "Cuidado: Error!",'message' : "No puede seleccionar como fecha de inicio dias pasados",}
                return res
            return res

	def onchange_final(self, cr, uid, ids, fh_final, context=None):
            """
            Onchange para validar que la fecha final no es menor a lafecha de creacion
            """
            res = {}
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if fh_final < now:
                res['warning'] = {'title': "Cuidado: Error!",'message' : "No puede seleccionar como fecha final dias pasados",}
                return res
            return res