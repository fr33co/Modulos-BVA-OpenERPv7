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

class gdc_sector(osv.Model):
    _name = "gdc.sector"
    _rec_name = "name_sector"
    _columns = {
            'name_sector' : fields.char(string="Sector", size=256, required=True),
    }
    
    _order="name_sector"
    
class gdc_caracterizacion(osv.Model):
    _name = "gdc.proyectos"
    _columns = {
            'codigo': fields.char(string="Codigo", size=20),  
            'actividad': fields.char(string="Actividad", size=64), 
            'cobertura': fields.selection((('n','Nacional'), ('R','Regional')),'Cobertura', required=True),
            'priority': fields.selection((('b','Baja'), ('n','Normal'), ('a', 'Alta')),'Prioridad', required=True),
            'estado': fields.selection((('n','No definido'), ('pro','Propuesto'), ('epl', 'En planificacion'), ('epro', 'En progreso'), ('c', 'Congelado'), ('t', 'Terminado'), ('plan', 'Plantilla'), ('ar', 'Archivado')),'Estado', required=True),
            'progreso': fields.char(string="Progreso", size=20), 
            'date_start': fields.datetime('Fecha estimada de inicio',select=True),
            'date_end': fields.datetime('Fecha estimada de finalizacion',select=True),
            'responsible_id' : fields.many2one('res.users', 'Responsable', required=True),
            'supervisor_id' : fields.many2one('res.company', 'Supervisor', required=True),
            'description': fields.text('Description'),
            'presu_tentativo': fields.integer('Presupuesto Tentativo'),
            'presu_real': fields.integer('Presupuesto Real'),
            'members': fields.many2many('res.company', 'project_company_rel', 'project_id', 'uid', 'Entes Ejecutantes'),
            
    }
    
    _defaults = {
            'supervisor_id': 1,
            'codigo': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'gdc.proyectos'),
            'estado': 'n',
            'progreso': '0.0%',
    }
