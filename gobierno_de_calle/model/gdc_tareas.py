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

##########
# Tareas #
##########
    
class gdc_tareas(osv.Model):
    """
    Modelo para gestionar las tareas de las actividades
    """
    _name = "gdc.tareas"
    _rec_name = "name_tarea"
    _order="name_tarea"

    def onchange_proyecto(self, cr, uid, ids, project_id2, context=None):
        values = {}
        if not project_id2:
            return values
        datos = self.pool.get('gdc.proyectos').browse(cr, uid, project_id2, context=context)
        values.update({
            'supervisor_id' : datos.supervisor_id.id,
            'responsible_id' : datos.responsible_id.id,
            'ejecutor_id' : datos.ejecutor_id.id,
            'date_start_proyecto' : datos.date_start,
            'date_end_proyecto' : datos.date_end,
            'estado_proyecto' : datos.estado,
        })
        return {'value' : values}

    def onchange_date_start_tarea(self, cr, uid, ids, project_id2, date_start_tarea, context=None):
        values = {}
        if not project_id2:
            return values
        datos = self.pool.get('gdc.proyectos').browse(cr, uid, project_id2, context=context)
        if date_start_tarea < datos.date_start:
            values['warning'] = {'title': "Cuidado: Error!",'message' : "No puede seleccionar fechas menores a la inicio del proyecto.",}
            return values
        else:
            return values

    def onchange_date_end_tarea(self, cr, uid, ids, project_id2, date_end_tarea, context=None):
        values = {}
        if not project_id2:
            return values
        datos = self.pool.get('gdc.proyectos').browse(cr, uid, project_id2, context=context)
        if date_end_tarea > datos.date_end:
            print date_end_tarea
            print datos.date_end
            values['warning'] = {'title': "Cuidado: Error!",'message' : "No puede seleccionar fechas mayores a la final del proyecto.",}
            return values
        else:
            return values


    def _compute_days_tarea(self, cr, uid, ids, field, arg, context=None):
        """
        Metodo para calcular los dias entre la fecha de inicio y la fecha final
        """
        import datetime
        result = {}
        records = self.browse(cr, uid, ids, context=context)
        for r in records:
            if r.date_start_tarea:
                d = time.strptime(r.date_start_tarea,'%Y-%m-%d %H:%M:%S')
        for r2 in records:
            if r2.date_end_tarea:
                c = time.strptime(r2.date_end_tarea,'%Y-%m-%d %H:%M:%S')
                delta = datetime.datetime(c[0], c[1], c[2]) - datetime.datetime(d[0], d[1], d[2])
                weeks, days = divmod(delta.days, 1)
            result[r2.id] = weeks
        return result
            
            
    _columns = {
        'name_tarea': fields.char(string="Tarea", size=50, required=True),
        'project_id2': fields.many2one('gdc.proyectos', 'Proyecto', required=True),
        'estado_tarea': fields.selection((('Planificado','Planificado'), ('Terminado', 'Terminado'), ('No concluida', 'No concluida')),'Estado', required=True),
        'estado_proyecto': fields.char(string="Estado (Proyecto)", required=False),
        'date_start_proyecto': fields.datetime('Fecha de inicio (Proyecto)',select=True),
        'date_start_tarea': fields.datetime('Fecha de inicio',select=True, required=True),
        'date_end_proyecto': fields.datetime('Fecha de finalizacion (Proyecto)',select=True),
        'date_end_tarea': fields.datetime('Fecha de finalizacion',select=True,required=True),
        'progreso_tarea': fields.float(string="Progreso de tarea"), 
        'dias_tarea': fields.function(_compute_days_tarea, type='char', string='Dias asignados a la tarea'),
        'responsible_id' : fields.many2one('res.users', 'Responsable asignado', domain=['|',('is_company','=',False),('category_id.name','ilike','Responsable')], required=False),
        'supervisor_id' : fields.many2one('res.company', 'Ente Supervisor', domain=[('category_id.name','ilike','Supervisor')], required=False),        
        'ejecutor_id' : fields.many2one('res.company', 'Ente Ejecutor', domain=[('category_id.name','ilike','Supervisor')], required=False),
        'members_tareas': fields.many2many('res.company', 'project_company_rel2', 'project_id2', 'uid2', 'Equipos de trabajo'),
        'description': fields.text('Description',required=True),
        'tipo_documento': fields.selection((('PDF','PDF'), ('DOC','DOC'), ('ODT','ODT'), ('XLS', 'XLS'), ('ODS','ODS')),'Tipo de documento', required=False),
        'adjunto_gaceta_pdf': fields.binary('Adjuntar Gaceta digital'),
        'adjunto_gaceta_name_pdf': fields.char('Adjuntar Gaceta digital'),
        'adjunto_gaceta_doc': fields.binary('Adjuntar Gaceta digital'),
        'adjunto_gaceta_name_doc': fields.char('Adjuntar Gaceta digital'),
        'adjunto_gaceta_odt': fields.binary('Adjuntar Gaceta digital'),
        'adjunto_gaceta_name_odt': fields.char('Adjuntar Gaceta digital'),
        'adjunto_gaceta_xls': fields.binary('Adjuntar Gaceta digital'),
        'adjunto_gaceta_name_xls': fields.char('Adjuntar Gaceta digital'),
        'adjunto_gaceta_ods': fields.binary('Adjuntar Gaceta digital'),
        'adjunto_gaceta_name_ods': fields.char('Adjuntar Gaceta digital'),
        'image1': fields.binary("Foto 1", help="Seleccione una imagen"),
        'image2': fields.binary("Foto 2", help="Seleccione una imagen"),
        'image3': fields.binary("Foto 3", help="Seleccione una imagen"),
        'image4': fields.binary("Foto 4", help="Seleccione una imagen"),
    }

    def _check_dates_tareas(self, cr, uid, ids, context=None):
        """
        SQL Constraints para validar que La fecha de inicio debe ser 
        menor que la fecha final
        """
        for leave in self.read(cr, uid, ids, ['date_start_tarea', 'date_end_tarea'], context=context):
            if leave['date_start_tarea'] and leave['date_end_tarea']:
                if leave['date_start_tarea'] > leave['date_end_tarea']:
                    return False
        return True
        
    def _check_dates_tarea_start(self, cr, uid, ids, context=None):
        """
        SQL Constraints para validar que La fecha de inicio debe ser 
        menor que la fecha final
        """
        for leave in self.read(cr, uid, ids, ['date_start_tarea', 'date_start_proyecto'], context=context):
            if leave['date_start_tarea'] and leave['date_start_proyecto']:
                if leave['date_start_tarea'] < leave['date_start_proyecto']:
                    return False
        return True
        
    def _check_dates_tarea_end(self, cr, uid, ids, context=None):
        """
        SQL Constraints para validar que La fecha de inicio debe ser 
        menor que la fecha final
        """
        for leave in self.read(cr, uid, ids, ['date_end_tarea', 'date_end_proyecto'], context=context):
            if leave['date_end_tarea'] and leave['date_end_proyecto']:
                if leave['date_end_tarea'] > leave['date_end_proyecto']:
                    return False
        return True

    _constraints = [
        (_check_dates_tareas, 'Error! La fecha de inicio debe ser menor que la fecha final.', ['date_start_tarea', 'date_end_tarea']),
        (_check_dates_tarea_start, 'Error! La fecha de inicio de la tarea no puede ser menor a la del proyecto.', ['date_start_tarea', 'date_start_proyecto']),
        (_check_dates_tarea_end, 'Error! La fecha final de la tarea no puede ser mayor a la del proyecto.', ['date_end_tarea', 'date_end_proyecto']),
    ]
    
    _defaults = {
            'estado_tarea': 'Planificado',
            'progreso_tarea': 0.0,
            'adjunto_gaceta_name_pdf': 'soporte.pdf',
            'adjunto_gaceta_name_doc': 'soporte.doc',
            'adjunto_gaceta_name_odt': 'soporte.odt',
            'adjunto_gaceta_name_xls': 'soporte.xls',
            'adjunto_gaceta_name_ods': 'soporte.ods',
    }

    def finish_tarea(self, cr, uid, ids, context=None):
        result = {}
        gdc_project = self.pool.get('gdc.proyectos')
        gdc_tareas = self.pool.get('gdc.tareas')
        self.write(cr, uid, ids, {'estado_tarea': 'Terminado', 'progreso_tarea': 100})
        for r in self.read(cr, uid, ids, ['project_id2'], context=context):
            qty_tareas_totales = len(gdc_tareas.search(cr, uid, [('project_id2', '=', r['project_id2'][0])], context=context))
            qty_tareas_ejecutadas_id = gdc_tareas.search(cr, uid, [('project_id2', '=', r['project_id2'][0])], context=context)
            tareas_rd = gdc_tareas.search(cr, uid, ['|', ('project_id2', '=', r['project_id2'][0]), ('id', 'in', qty_tareas_ejecutadas_id), ('estado_tarea', '=', 'Terminado')], context=context)
            tareas_terminadas = len(tareas_rd)
            porcentaje = (100 * tareas_terminadas) / qty_tareas_totales
            gdc_project.write(cr, uid, r['project_id2'][0], {'estado': 'Progreso', 'progreso': porcentaje})

