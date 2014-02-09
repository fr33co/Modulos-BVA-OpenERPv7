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

###############
# Incidencias #
###############
    
class gdc_incidencias(osv.Model):
    """
    Modelo para gestionar las tareas de las actividades
    """
    _name = "gdc.incidencias"
    _rec_name = "name_incidencia"
    _order="name_incidencia"
    
    def onchange_tarea(self, cr, uid, ids, tarea_id, context=None):
        values = {}
        gdc_tareas = self.pool.get('gdc.tareas')
        tareas_brw = gdc_tareas.browse(cr, uid, tarea_id, context=context)
        values.update({
        'project_id' : tareas_brw.project_id2.id,
        })
        return {'value' : values}

    _columns = {
        'name_incidencia': fields.char(string="Incidencia", size=50, required=False),
        'tarea_id': fields.many2one('gdc.tareas', 'tarea', required=False),
        'reporter_id' : fields.many2one('res.users', 'Usuario', required=True),
        'project_id': fields.many2one('gdc.proyectos', 'tarea', required=False),
        'date_reporter': fields.datetime('Fecha',select=True, required=True),
        'description': fields.text('Description'),
    }

    _defaults = {
        'reporter_id': lambda s, cr, uid, c: uid,
    }
