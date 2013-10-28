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

class gdc_sector(osv.Model):
    _name = "gdc.sector"
    _rec_name = "name_sector"
    _columns = {
            'name_sector' : fields.char(string="Sector", size=256, required=True),
    }
    
    _order="name_sector"
        
class gdc_tareas(osv.Model):
    _name = "gdc.tareas"
    _rec_name = "name_tarea"
    _columns = {
        'name_tarea': fields.char(string="Tarea", size=50, required=False),
        'project_id2': fields.many2one('gdc.proyectos', 'Asignacion', required=False),
        'date_start_tarea': fields.datetime('Fecha de inicio',select=True),
        'date_end_tarea': fields.datetime('Fecha de finalizacion',select=True),
        'progreso_tarea': fields.char(string="Progreso de tarea", size=20), 
        'responsible_id' : fields.many2one('res.users', 'Responsable asignado', domain=['|',('is_company','=',False),('category_id.name','ilike','Responsable')], required=False),
        'members_tareas': fields.many2many('res.company', 'project_company_rel2', 'project_id2', 'uid2', 'Entes Encargados'),
        'description': fields.text('Description'),
        'informe_tareas': fields.binary('Informe'),
        'image': fields.binary("Foto", help="Seleccione una imagen"),
    }
    
    _order="name_tarea"
    
class gdc_proyectos(osv.Model):
    _name = "gdc.proyectos"
    _rec_name = "actividad"
    
    def on_change_address_id(self, cr, uid, ids, address_id, context=None):
        values = {}
        if not address_id:
            return values
        address = self.pool.get('res.partner').browse(cr, uid, address_id, context=context)
        values.update({
            'street' : address.street,
            'street2' : address.street2,
            'city' : address.city,
            'country_id' : address.country_id and address.country_id.id or False,
            'state_id' : address.state_id and address.state_id.id or False,
            'zip' : address.zip,
        })
        return {'value' : values}
    
    def onchange_date_start(self, cr, uid, ids, date_start, context=None):
        res = {}
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')        
        if date_start < now:
            res['warning'] = {'title': "Cuidado: Error!",'message' : "No puede seleccionar como fecha de inicio dias pasados",}
            return res
        return res
        
    def onchange_date_end(self, cr, uid, ids, date_end, context=None):
        res = {}
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if date_end < now:
            res['warning'] = {'title': "Cuidado: Error!",'message' : "No puede seleccionar como fecha final dias pasados",}
            return res
        return res
        
    def _compute_days(self, cr, uid, ids, field, arg, context=None):
        import datetime
        result = {}
        records = self.browse(cr, uid, ids, context=context)
        for r in records:
            if r.date_start:
                d = time.strptime(r.date_start,'%Y-%m-%d %H:%M:%S')
        for r2 in records:
            if r2.date_end:
                c = time.strptime(r2.date_end,'%Y-%m-%d %H:%M:%S')
                delta = datetime.datetime(c[0], c[1], c[2]) - datetime.datetime(d[0], d[1], d[2])
                weeks, days = divmod(delta.days, 1)
            result[r2.id] = weeks
        return result

    _columns = {
            'date_created': fields.char('Fecha de Creación',select=True, readonly=True),
            'codigo': fields.char(string="Codigo", size=20),  
            'actividad': fields.char(string="Actividad", size=64, required=True), 
            'cobertura': fields.selection((('Nacional','Nacional'), ('Regional','Regional'), ('Municipal', 'Municipal')),'Cobertura', required=True),
            'priority': fields.selection((('Baja','Baja'), ('Normal','Normal'), ('Alta', 'Alta')),'Prioridad', required=True),
            'estado': fields.selection((('Borrador','Borrador'), ('Propuesto','Propuesto'), ('Planificacion', 'Planificacion'), ('Progreso', 'Progreso'), ('Congelado', 'Congelado'), ('Terminado', 'Terminado'), ('Plantilla', 'Plantilla'), ('Archivado', 'Archivado'), ('Vencido', 'Vencido')),'Estado', required=True),
            'progreso': fields.char(string="Progreso", size=20), 
            'dias_proyecto': fields.function(_compute_days, type='char', string='Dias asignados al proyecto'),
            'date_start': fields.datetime('Fecha estimada de inicio',select=True, required=True),
            'date_end': fields.datetime('Fecha estimada de finalizacion',select=True, required=True),
            'responsible_id' : fields.many2one('res.users', 'Responsable asignado', domain=[('category_id.name','ilike','Responsable')], required=True),
            'supervisor_id' : fields.many2one('res.company', 'Ente Supervisor', domain=[('category_id.name','ilike','Supervisor')], required=True),
            'description': fields.text('Description'),
            'presu_tentativo': fields.integer('Presupuesto Tentativo'),
            'presu_real': fields.integer('Presupuesto Real'),
            'bene_tentativo': fields.integer('Cantidad de beneficiados tentativos'),
            'members_project': fields.many2many('res.company', 'project_company_rel', 'project_id', 'uid', 'Entes Encargados'),
            'address_id': fields.many2one('res.partner','Lugar', readonly=False, required=True, domain=[('category_id.name','ilike','Lugar')]),
            'street': fields.related('address_id','street',type='char',string='Direccion'),
            'street2': fields.related('address_id','street2',type='char',string='Cont. Direccion'),
            'state_id': fields.related('address_id','state_id',type='many2one', relation="res.country.state", string='Estado'),
            'zip': fields.related('address_id','zip',type='char',string='Codigo Postal'),
            'city': fields.related('address_id','city',type='char',string='Ciudad'),
            'country_id': fields.related('address_id', 'country_id', type='many2one', relation='res.country', string='Pais', readonly=False),
            'tareas_ids': fields.one2many('gdc.tareas', 'project_id2', string="Tareas"),
    }
        
    _order="actividad"
    
    def _check_dates(self, cr, uid, ids, context=None):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for leave in self.read(cr, uid, ids, ['date_start', 'date_end'], context=context):
            if leave['date_start'] and leave['date_end']:
                if leave['date_start'] > leave['date_end']:
                    return False
        return True

    _constraints = [
        (_check_dates, 'Error! La fecha de inicio debe ser menor que la fecha final.', ['date_start', 'date_end'])
    ]
    
    _defaults = {
            'supervisor_id': 1,
            'codigo': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'gdc.proyectos'),
            'estado': 'Borrador',
            'progreso': '0.0%',
            'date_created': lambda *a: datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
            'dias_proyecto': 'Aun no asignados. ',
    }
