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
from datetime import datetime
import time
from openerp.osv import osv, fields
from tools.translate import _

############################
# Fondos de financiamiento #
############################

class gdc_fondos(osv.Model):
    """
    Modelo para gestionar los fondos de financiamiento
    """
    _name = "gdc.fondos"
    _rec_name = "name"
    _order="name"

    _columns = {
        'name': fields.char(string="Fondo de financiamiento", size=64, required=True), 
    }
