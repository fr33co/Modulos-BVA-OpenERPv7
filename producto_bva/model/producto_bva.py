from openerp.osv import osv, fields

class producto_bva(osv.Model):

	_inherit = "product.product"
	_columns = {
        'g' : fields.char(string="G", size=2, required=True),
        'sg' : fields.char(string="S/G", size=2, required=True),
        's' : fields.char(string="S", size=2, required=True),
        'estado' : fields.selection((('1','Bueno'), ('2','Malo')),'Status', required=True),
        }