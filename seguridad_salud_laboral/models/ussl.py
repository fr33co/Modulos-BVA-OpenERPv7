# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class hr_holidays(osv.Model):
    _inherit = "hr.holidays"
    
    _columns = {
        'name_diseases_type_id' : fields.many2one('hr.holidays.diseases.types', string="Tipo de Enfermedad", change_default=True, select=True, ondelete='cascade', required=False),
        'name_diseases_id' : fields.many2one('hr.holidays.diseases', string="Enfermedad", change_default=True, select=True, ondelete='cascade', required=False),
    }

class hr_holidays_diseases_types(osv.Model):
    _name = "hr.holidays.diseases.types"
    _order = "type_diseases"
    _rec_name = "type_diseases"
    
    _columns = {
        'type_diseases' : fields.char(string="Tipo de Enfermedad", required=True),
    }

class hr_holidays_diseases(osv.Model):
    _name = "hr.holidays.diseases"
    _order = "name_diseases"
    _rec_name = "name_diseases"
    
    _columns = {
        'name_diseases' : fields.char(string="Enfermedad", required=True),
        'name_diseases_type_id' : fields.many2one('hr.holidays.diseases.types', string="Tipo de Enfermedad", required=True)
    }
    
