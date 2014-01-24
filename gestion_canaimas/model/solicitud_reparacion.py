# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class solicitud_reparacion(osv.Model):
    _name = "solicitud.reparacion"
    _order = 'c_solicitud'
    _rec_name = 'c_solicitud'

    def on_change_datos(self, cr, uid, ids, c_solicitud, context=None):
        values = {}
        solicitud_soporte = self.pool.get('solicitud.soporte')
        if not c_solicitud:
            return values
        datos = solicitud_soporte.browse(cr, uid, c_solicitud, context=context)
        print datos.id
        values.update({
            'serial' : datos.serial,
            'modelo' : datos.modelo.modelo,
            'status_ss' : datos.status,
            'descripcion' : datos.descripcion,
            'f_solicitud': datos.f_solicitud,
            'f_entrega': datos.f_entrega,
            'status': 'Atendiendo',
        })
        solicitud_soporte.write(cr, uid, datos.id, {'status': 'Atendiendo'})
        return {'value' : values}
        
        
    _columns = {
        'c_solicitud' : fields.many2one('solicitud.soporte', 'Código de Solicitud', required=True),
        'f_solicitud': fields.char('Fecha de Solicitud', readonly=False),
        'f_entrega': fields.date('Fecha de Entrega', readonly=False),
        'serial' : fields.char(string="Serial", readonly=False),
        'modelo' : fields.char(string="Modelo", size=25, readonly=False),
        'status_ss' : fields.char(string="Status de la solicitud", size=25, readonly=False),
        'descripcion' : fields.text(string="Descripción del Problema", readonly=False),
        'tecnico' : fields.many2one('res.users', 'Técnico', required=True, readonly=True),
        'solucion' : fields.text(string="Solución", required=True),
        'status': fields.selection((('Revisar','Revisar'),('Atendiendo','Atendiendo'),('Reparada','Reparada'), ('Remitida','Remitida'), ('Entregada','Entregada')),'Status Soporte', required=True),
        }
    
    _defaults = {
        'tecnico': lambda s, cr, uid, c: uid,
        'status': 'Revisar',
    }       

        
        
