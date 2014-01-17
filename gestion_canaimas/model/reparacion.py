# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class registrar_sede(osv.Model):
	_name = "reparacion"

	_columns = {
        'serial' : fields.char(string="Serial Canaima", readonly=True),
        'modelo' : fields.char(string="modelo", size=25, readonly=True),
        'nombre' : fields.char(string="Nombre", size=25, readonly=True),
        'apellido' : fields.char(string="Apellido", size=25, readonly=True),
        'nombre_r' : fields.char(string="Nombre Representante", size=25, readonly=True),
        'apellido_r' : fields.char(string="Apellido Representante", size=25, readonly=True),
        'telefono' : fields.char(string="Teléfono", size=11, readonly=True),
        'descripcion' : fields.text(string="Descripción del Problema", readonly=True),
        'c_solicitud' : fields.many2one('solicitud', 'Código de Solicitud',required=True),
        'f_solicitud': fields.char('Fecha de Solicitud', readonly=True),
        'f_entrega': fields.date('Fecha de Entrega', readonly=True),
        'tecnico' : fields.many2one('res.users', 'Técnico a cargo', required=True),
        'solucion' : fields.text(string="Solución"),
        'estado' : fields.selection((('Reparada','Reparada'), ('En Espera','En Espera'), ('Remitida','Remitida')),'Estado de la Canaima', required=False),
        }

        def on_change_datos(self, cr, uid, ids, c_solicitud, context=None):

            values = {}
            if not c_solicitud:
                return values
            datos = self.pool.get('solicitud').browse(cr, uid, c_solicitud, context=context)
            values.update({
                'serial' : datos.serial,
                'modelo' : datos.modelo,
                'nombre' : datos.nombre,
                'apellido' : datos.apellido,
                'nombre_r' : datos.nombre_r,
                'apellido_r' : datos.apellido_r,
                'telefono' : datos.telefono,
                'descripcion' : datos.descripcion,
                'c_solicitud' : datos.c_solicitud,
                'f_solicitud': datos.f_solicitud,
                'f_entrega': datos.f_entrega,
            })
            return {'value' : values}