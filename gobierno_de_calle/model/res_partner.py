from openerp.osv import osv, fields


class Partner(osv.Model):
    _inherit = 'res.partner'
    _columns = {
        'locacion' : fields.boolean("Es un lugar?"),
    }

    _defaults = {
        'locacion': False,
    }
