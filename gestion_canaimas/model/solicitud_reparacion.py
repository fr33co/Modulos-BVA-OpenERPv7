# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class solicitud_reparacion(osv.Model):
    _name = "solicitud.reparacion"
    _order = 'c_solicitud'
    _rec_name = 'c_solicitud'
    
    _columns = {
        'c_solicitud' : fields.many2one('solicitud.soporte', 'Código de Solicitud', required=True),
        'f_solicitud': fields.char('Fecha de Solicitud', readonly=True),
        'f_entrega': fields.date('Fecha de Entrega', readonly=True),
        'serial' : fields.char(string="Serial", readonly=True),
        'modelo' : fields.char(string="Modelo", size=25, readonly=True),
        'status_ss' : fields.char(string="Status de la solicitud", size=25, readonly=True),
        'descripcion' : fields.text(string="Descripción del Problema", readonly=True),
        'tecnico' : fields.many2one('res.users', 'Técnico', required=True),
        'solucion' : fields.text(string="Solución"),
        'status': fields.selection((('Revisar','Revisar'),('Atendiendo','Atendiendo'),('Reparada','Reparada'), ('Remitida','Remitida')),'Status Soporte', required=True)
        }
        
    def on_change_datos(self, cr, uid, ids, c_solicitud, context=None):
        values = {}
        if not c_solicitud:
            return values
        datos = self.pool.get('solicitud.soporte').browse(cr, uid, c_solicitud, context=context)
        values.update({
            'serial' : datos.serial,
            'modelo' : datos.modelo,
            'status_ss' : datos.status,
            'descripcion' : datos.descripcion,
            'f_solicitud': datos.f_solicitud,
            'f_entrega': datos.f_entrega,
        })
        return {'value' : values}
