# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class Municipio(osv.Model):
    _name = "configuracion.municipio"
    _columns = {
        'estado' : fields.many2one('configuracion.estado','Estado',ondelete='cascade',required=True),
        'municipio' : fields.char(string="Municipio",size=100, required=True),
    }
    _order='estado'
    _rec_name='municipio'
