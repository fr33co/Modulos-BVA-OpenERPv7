###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP Venezuela (<http://openerp.com.ve>).
#    All Rights Reserved
###############Credits######################################################
#    Coded by: Vauxoo C.A.           
#    Planified by: Nhomar Hernandez
#    Audited by: Vauxoo C.A.
#############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
from openerp.osv import osv, fields
from tools.translate import _

class res_partner(osv.Model):
    
    def _get_city_name(self, cr, uid, ids, field_name, arg, context=None):
        if context is None:
            context={}
        res={}
        for obj in self.browse(cr, uid, ids):
            if obj.city_id:
                res[obj.id] = obj.city_id.name
            else:
                res[obj.id] = ''
        return res

    _inherit='res.partner'
    _columns = {
        'municipality_id':fields.many2one('res.country.municipality','Municipality', help="In this field enter the name of the municipality which is associated with the parish", domain= "[('state_id','=',state_id)]"),
        'parish_id':fields.many2one('res.country.parish','Parish',help="In this field you enter the parish to which the sector is associated",domain= "[('municipalities_id','=',municipality_id)]" ),
        'zipcode_id':fields.many2one('res.country.zipcode',string='Zip Code',help="in this field is selected Zip Code associated with this sector"),
        #~ 'sector_id':fields.many2one('res.country.sector',string='Sector',required=False,help="in this field select the Sector associated with this Municipality"),
        'city_id':fields.many2one('res.country.city',string='City',domain= "[('state_id','=',state_id)]",help="in this field select the city associated with this State"),
        'city':fields.function(_get_city_name, method=True, type='char', string='City', size=256, domain= "[('state_id','=',state_id)]",store=True),
    }

