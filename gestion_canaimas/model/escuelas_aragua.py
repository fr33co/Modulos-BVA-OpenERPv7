# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class escuelas_edo_aragua(osv.Model):
    _name = "escuelas"
    _order = 'municipio'
    _rec_name = 'escuela'
    
    _columns = {
        'pais' : fields.many2one('res.country', 'Pais', required=True),
        'estado' : fields.many2one('res.country.state', 'Estado', required=True),
        'municipio' : fields.many2one('res.country.municipality', 'Municipio', required=True),
        'escuela' : fields.char(string="Nombre de la escuela", size=150, required=True),
        'd_escuela' : fields.text(string="Dirección Escuela", required=True),
        }

    _defaults = {
        'pais': 240,
    }