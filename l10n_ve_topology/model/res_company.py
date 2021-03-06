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

class res_company(osv.Model):
    
    _inherit ='res.company'

    _columns = {
        'city_id': fields.many2one('res.country.city', 'Ciudad', required=True),
        'municipality_id': fields.many2one('res.country.municipality', 'Municipio', required=True),
        'parish_id': fields.many2one('res.country.parish', 'Parroquia', required=True),
        'sector_id': fields.many2one('res.country.sector', 'ZIP', required=False),
        'zipcode_id': fields.many2one('res.country.zipcode', 'ZIP', required=False),
    }
