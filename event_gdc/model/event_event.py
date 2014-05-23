#-*- coding:utf-8 -*-
##############################################################################
#
#
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
#
##############################################################################

from openerp.osv import osv, fields

class event_event(osv.Model):
    _inherit = 'event.event'
    _columns = {
        'acuerdos': fields.text('Acuerdos', readonly=False, states={'done': [('readonly', True)]}),
        'conclusiones': fields.text('Conclusiones', readonly=False, states={'done': [('readonly', True)]}),
        'visible_grupo': fields.boolean('¿Seleccionar instituciones?'),
        'address_id': fields.many2one('res.partner','Lugar', readonly=False, required=True, domain=[('category_id.name','ilike','Lugar')]),
        'members_project': fields.many2many('res.company', 'project_company_rel', 'project_id', 'uid', 'Instituciones'),
        'street': fields.related('address_id','street',type='char',string='Direccion'),
        'street2': fields.related('address_id','street2',type='char',string='Cont. Direccion'),
        'state_id': fields.related('address_id','state_id',type='many2one', relation="res.country.state", string='Estado'),
        'zipcode_id': fields.related('address_id','zipcode_id',type='many2one', relation="res.country.zipcode", string='Zipcode'),
        'city_id': fields.related('address_id','city_id',type='many2one', relation="res.country.city", string='City'),
        'municipality_id': fields.related('address_id','municipality_id',type='many2one', relation="res.country.municipality", string='Municipality'),        
        'parish_id': fields.related('address_id','parish_id',type='many2one', relation="res.country.parish", string='Parish'),
        'sector_id': fields.related('address_id','sector_id',type='many2one', relation="res.country.sector", string='Sector'),
        'country_id': fields.related('address_id', 'country_id', type='many2one', relation='res.country', string='Pais', readonly=False),
    }
