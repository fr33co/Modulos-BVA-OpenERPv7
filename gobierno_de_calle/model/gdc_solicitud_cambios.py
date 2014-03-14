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
# Cambios     #
###############

class gdc_solicitud_proyectos(osv.Model):
    """
    Modelo para gestionar las tareas de las actividades
    """
    _name = "gdc.solicitud.proyectos"
    _rec_name = "project_id"
    _order="project_id"
    
    _columns = {
        'project_id': fields.many2one('gdc.proyectos', 'Proyecto', required=False),
        'justification': fields.text('Justificacion'),
        'date': fields.datetime('Fecha solicitud',select=True),
        'user_id' : fields.many2one('res.users', 'Usuario', required=False),
        'solicitud': fields.selection((('En espera','En espera'), ('Aprobar','Aprobar'), ('Denegar', 'Denegar')),'Status', required=False),
    }
    

class gdc_solicitud_tareas(osv.Model):
    """
    Modelo para gestionar las tareas de las actividades
    """
    _name = "gdc.solicitud.tareas"
    _rec_name = "tarea_id"
    _order="tarea_id"
    
    _columns = {
        'tarea_id': fields.many2one('gdc.tareas', 'Tarea', required=False),
        'justification': fields.text('Justificacion'),
        'date': fields.datetime('Fecha solicitud',select=True),
        'user_id' : fields.many2one('res.users', 'Usuario', required=False),
        'solicitud': fields.selection((('En espera','En espera'), ('Aprobar','Aprobar'), ('Denegar', 'Denegar')),'Status', required=False),
    }
