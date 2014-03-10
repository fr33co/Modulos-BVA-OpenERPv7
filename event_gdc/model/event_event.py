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
    }
