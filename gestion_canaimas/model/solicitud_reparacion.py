# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class solicitud_reparacion(osv.Model):

    # Nombre de el Objeto
    _name = "solicitud.reparacion"

    # Se Ordena por Codigo de solicitud  
    _order = 'c_solicitud'
   # _rec_name = ''

    """
    Metodo que trae la informacion de las solicitud de soporte de la clase solicitud_soporte
    al formulario de solicitud de reparación.
    """
    def on_change_datos(self, cr, uid, ids, c_solicitud, context=None):
        values = {}
        if not c_solicitud:
            return values
        datos = self.pool.get('solicitud.soporte').browse(cr, uid, c_solicitud, context=context)
        entrega = datos.f_entrega.split("-")
        fecha2= entrega[2]+"/"+entrega[1]+"/"+entrega[0]
        values.update({
            'serial' : datos.serial,
            'modelo' : datos.modelo.modelo,
            'status_ss' : datos.status,
            'descripcion' : datos.descripcion,
            'f_solicitud': datos.f_solicitud,
            'f_entrega': fecha2,
        })
        return {'value' : values}

    """
    Metodo que al cambiar el estado de la solicitud en el objeto solicitud_reparacion cambia
    automaticamente en el objeto solicitud_soporte y tambien envia la Solucion o diagnostico 
    del Problema.
    """
    def actualizar_status(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=None)
        obj_estado = self.pool.get('solicitud.soporte')
        estado_s = self.browse(cr, uid, ids)[0]
        for r2 in obj:
            rd_estado = obj_estado.read(cr, uid, r2.c_solicitud.id, context=context)
            resultado = rd_estado['c_solicitud']
            status2  = estado_s.status
            solucionc = estado_s.solucion
            tecnicos = estado_s.tecnico
            cr.execute("UPDATE solicitud_soporte SET status=%s, solucion=%s WHERE c_solicitud=%s;", (status2, solucionc, resultado,))
        return True

    _columns = {
        'c_solicitud' : fields.many2one('solicitud.soporte', 'Código de Solicitud', domain="[('status','ilike','Atendiendo')]", required=True),
        'f_solicitud': fields.char('Fecha de Solicitud', readonly=False),
        'f_entrega': fields.char('Fecha de Entrega', readonly=False),
        'serial' : fields.char(string="Serial", readonly=False),
        'modelo' : fields.char(string="Modelo", readonly=False),
        'status_ss' : fields.char(string="Status de la solicitud", readonly=False),
        'descripcion' : fields.text(string="Descripción del Problema", readonly=False),
        'tecnico' : fields.many2one('res.users', 'Técnico', required=False, readonly=False),
        'solucion' : fields.text(string="Solución", required=True),        
        'hardware' : fields.boolean('Hardware'),
        'software' : fields.boolean('Software'),
        'status': fields.selection([('Reparada','Reparada'), ('Remitir','Remitir')], string="Estado de Solicitud"),
        }
    
    # Se declara que por defecto el campo Técnico cargue el nombre del usuario logeado
    _defaults = {
        'tecnico': lambda s, cr, uid, c: uid,
    }       


