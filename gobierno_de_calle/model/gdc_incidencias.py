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
    
    def onchange_proyecto(self, cr, uid, ids, project_id, context=None):
        values = {}
        if not project_id:
            return values
        datos = self.pool.get('gdc.proyectos').browse(cr, uid, project_id, context=context)
        values.update({
            'date_start_proyecto' : datos.date_start,
            'date_end_proyecto' : datos.date_end,
            'state_proyecto' : datos.estado,
        })
        return {'value' : values}
        
    def onchange_tarea(self, cr, uid, ids, tarea_id, context=None):
        values = {}
        if not tarea_id:
            return values
        datos = self.pool.get('gdc.tareas').browse(cr, uid, tarea_id, context=context)
        values.update({
            'project_id' : datos.project_id2.id,
            'date_start_tarea' : datos.date_start_tarea,
            'date_end_tarea' : datos.date_end_tarea,
            'state_tarea' : datos.estado_tarea,
        })
        return {'value' : values}

    def onchange_solicitud_cambio(self, cr, uid, ids, tarea_id, solicitud_cambio, context=None):
        values = {}
        if not tarea_id:
            return values
        datos = self.pool.get('gdc.tareas').browse(cr, uid, tarea_id, context=context)
        solicitud_obj = self.pool.get('gdc.solicitud.cambios')
        if solicitud_cambio == 'Proyecto':
            solicitud_obj.write(cr, uid, ids, {'project_id': datos.project_id2.id})
        else:
            solicitud_obj.write(cr, uid, ids, {'tarea_id': tarea_id})

    _columns = {
        'name_incidencia': fields.char(string="Incidencia", size=50, required=True),
        'tarea_id': fields.many2one('gdc.tareas', 'Tarea', required=False),
        'date_start_tarea': fields.datetime('Fecha de inicio',select=True),
        'date_start_proyecto': fields.datetime('Fecha de inicio',select=True),
        'date_end_tarea': fields.datetime('Fecha de finalizacion',select=True),
        'date_end_proyecto': fields.datetime('Fecha de finalizacion',select=True),
        'state_tarea': fields.char(string="Estado de la tarea", required=False),
        'state_proyecto': fields.char(string="Estado de la tarea", required=False),
        'reporter_id' : fields.many2one('res.users', 'Usuario', required=True),
        'project_id': fields.many2one('gdc.proyectos', 'Proyecto', required=False),
        'date_reporter': fields.datetime('Fecha',select=True, required=True),
        'description': fields.text('Description'),
        'verificar_solicitud': fields.boolean('¿Desea congelar el proceso?'),
        'selec_pro_tar': fields.selection((('Proyecto','Proyecto'), ('Tarea', 'Tarea')),'Desea notificar incidencia a:', required=True),
    }

    _defaults = {
        'reporter_id': lambda s, cr, uid, c: uid,
        'date_reporter': fields.date.context_today,
    }
