from openerp.osv import osv, fields

#Clase Informacion opcional
class info_opcional(osv.Model):
	#_inherit
	_name = "info.opcional"

	_columns = {
		'facebook' : fields.char(string="Facebook", size=35),
		'twitter' : fields.char(string="Twitter", size=35),	
	}