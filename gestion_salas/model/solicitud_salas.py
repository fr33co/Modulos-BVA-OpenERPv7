import time
import random
from openerp.osv import osv, fields
from datetime import datetime, timedelta

#Clase solicitud de sala
class Solicitar_Sala(osv.Model):
	_name = "solicitar.sala"
	_order = 'c_solicitud'
	_rec_name = 'c_solicitud'
	_columns = {
		'nombre' : fields.char(string="Nombre", size=25, required=True),
		'apellido' : fields.char(string="Apellido", size=25, required=True),
		'cedula' : fields.char(string="Cedula", size=8, required=True),
		'c_solicitud' : fields.char(string="Codigo de Solicitud", size=8, readonly=False, required=True),
		'fh_inicio' : fields.datetime(string="Fecha/Hora Inicio", required=True),
		'motivo':fields.many2one('actividades', 'Actvidad a realizar',required=False),
		#'motivo' : fields.selection((('1','Exposicion'), ('2','Reunion'), ('3', 'Cine Foro'), ('4','Charla'),('5','Presentacion de Tesis')),'Actvidad a realizar', required=False),
		'fh_final' : fields.datetime(string="Fecha/Hora Conclusion", required=True),
		'descripcion' : fields.text(string="Descripcion"),
		'telefono' : fields.char(string="Telefono Recidencia", size=11),
		'celular' : fields.char(string="Celular", size=11, required=True),
		#'salas': fields.char(string="Salas", size=25, required=False), 
		'salas':fields.many2one('registrar', 'Salas',required=True),
		'f_solicitud': fields.datetime('Fecha de Solicitud', readonly=True,  required=True),
		'facebook' : fields.char(string="Facebook", size=35),
		'twitter' : fields.char(string="Twitter", size=35),
		'facebook' : fields.char(string="Facebook", size=35),
		'correo' : fields.char(string="Correo Electronico", size=35),
		'ciudad' : fields.char(string="Ciudad", size=25),
		'estado' : fields.char(string="Estado", size=25),
		'municipio' : fields.char(string="Municipio", size=25),
		'parroquia' : fields.char(string="Parroquia", size=25),
		'sector' : fields.char(string="Sector", size=25),
		#'states' :fields.selection([('Solicitud','Solicitud'), ('Validada','Validada'), ('Rechazada', 'Rechazada')], string="Estado de Solicitud"),
	}
	def _get_last_id(self, cr, uid, ids, context = None):

                sfl_id       = self.pool.get('solicitar.sala')
                srch_id      = sfl_id.search(cr,uid,[])
                rd_id        = sfl_id.read(cr, uid, srch_id, context=context)
                if rd_id:
                    id_documento = rd_id[-1]['c_solicitud']
                    c_solicitud = id_documento[2:]
                    last_id      = c_solicitud.lstrip('0')
                    str_number   = str(int(last_id) + 1)
                    last_id      = str_number.rjust(5,'0')
                    codigo      = 'SS'+last_id
                else :
                    str_number = '1'
                    last_id      = str_number.rjust(5,'0')
                    codigo      = 'SS'+last_id
                return codigo

	_defaults = {
        #'c_solicitud': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'solicitar.sala'),
        'f_solicitud': lambda *a: time.strftime('%Y-%m-%d %I:%M:%S'),
        'c_solicitud' : _get_last_id
        #'states': 'Solicitud',
    } 

	def on_change_direccion(self, cr, uid, ids, salas, context=None):
	
	        values = {}
	        if not salas:
	            return values
	        direccion = self.pool.get('registrar').browse(cr, uid, salas, context=context)
	        values.update({
	            'estado' : direccion.estado,
	            'ciudad' : direccion.ciudad,
	            'municipio' : direccion.municipio,
	        })
	        return {'value' : values}

	def onchange_fh_final(self, cr, uid, ids, fh_final, context=None):

			res = {}
			now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			if fh_final < now:
				res['warning'] = {'title': "Atencion: Error!",'message' : "No puede seleccionar como fecha finaldias anteriores a hoy",}
				return res
			return res	        

	def onchange_fh_inicio(self, cr, uid, ids, fh_inicio, context=None):
			res = {}
			now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			if fh_inicio < now:
				res['warning'] = {'title': "Cuidado: Error!",'message' : "No puede seleccionar como fecha de inicio dias pasados",}
				return res
			return res

	# def on_change_cedula(self, cr, uid, ids, cedula, context=None):
	
	#         values = {}
	#         if not cedula:
	#             return values
	#         datos = self.pool.get('solicitar.sala')
	#         srch_partida =  datos.search(cr, uid, [('cedula','=', cedula)])
	#         rd_partida   = datos.read(cr, uid, srch_partida, context=context)
	#         nombre  = rd_partida[0]['nombre']
	#         apellido  = rd_partida[0]['apellido']
 #        	values.update({
 #                'nombre' : nombre, 'apellido' : apellido,
 #        	})
	#         print rd_partida 
	#         return {'value' : values}

	def on_change_cedula(self, cr, uid, ids, cedula, context=None):
	        values  = {}
	        valores = {}

	        valores = {
						        'nombre' : None,
								'apellido' : None,
								'telefono' : None,
								'celular' : None,
                            }

	        if not cedula:
	            return values

	        sfl_get_row    = self.pool.get('solicitar.sala')

	        srcnt_get_row = sfl_get_row.search_count(cr,uid,[('cedula','=',cedula)], context=None)

	        if srcnt_get_row > 0:
	            srch_get_row = sfl_get_row.search(cr,uid,[('cedula','=',cedula)])
	            rd_get_row    = sfl_get_row.read(cr, uid, srch_get_row,context=context)
	            valores = {
	                                'nombre': rd_get_row[0]['nombre'],
	                                'apellido': rd_get_row[0]['apellido'],
	                                'telefono': rd_get_row[0]['telefono'],
	                                'celular': rd_get_row[0]['celular'],
	                            }

	        values.update(valores)
	        return {'value' : values}