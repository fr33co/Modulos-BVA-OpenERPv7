from openerp.osv import osv, fields


class Partner(osv.Model):
    _inherit = 'res.partner'
    _columns = {
        'twitter': fields.char('Cuenta Twitter', size=34, required=False),
    }
