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

{
    'name' : "Gobierno de Calle",
    'category' : "Gestion",
    'version' : "1.0",
    'depends' : ['base', 'event_gdc', 'l10n_ve_topology'],
    'author' : "Angel A. Guadarrama B.",
    'description' : """
                    """,
    'data' : [
        'view/secuencia.xml',
        'view/gobiernodecalle_view.xml',
        'view/res_partner_view.xml',
        'view/res_company_view.xml',
        'view/res_users_view.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/tags.xml',
    ],
}
