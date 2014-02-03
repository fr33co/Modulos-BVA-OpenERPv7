#!/usr/bin/python
# -*- encoding: utf-8 -*-
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

class res_country_sector(osv.Model):
    
    _name = 'res.country.sector'
    _description = 'Sector'

    _columns = {
        'name': fields.char('Sector', size=128, required=True,help="In this field enter the name of the Sector"),
        'city':fields.related('city_id',type="many2one",required=True,relation='res.partner',help="In this field you enter the city to which the sector is associated"),
        'municipality':fields.related('municipality_id',type="many2one",relation='res.partner',required=True, help="In this field enter the name of the municipality which is associated with the parish"),
        'parish':fields.related('parish_id',type="many2one",required=True,relation='res.partner',help="In this field you enter the parish to which the sector is associated"),
        'zipcode':fields.related('zipcode_id',type="many2one",string='Zip Code',relation='res.partner',required=True,help="in this field is selected Zip Code associated with this sector"),
        'state':fields.related('state_id',type="many2one",required=True, relation='res.partner',help="In this field enter the name of state associated with the country"),
        'country':fields.related('country_id',type="many2one",required=True, relation='res.partner',help="In this field enter the name of Country"),
    }
