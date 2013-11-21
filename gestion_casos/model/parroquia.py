# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class Parroquia(osv.Model):
    _name    = "configuracion.parroquia"
    _columns = {
    'estado': fields.related('municipio','estado', type = 'many2one',relation = 'configuracion.estado',string = 'Estado'),
    'municipio':  fields.many2one('configuracion.municipio', 'Municipio'),
    'parroquia' : fields.char(string="Parroquia",size=100, required=True),
    }
    _order='municipio'
    _rec_name='parroquia'
