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

class gdc_fases(osv.Model):
    _name = "gdc.fases"
    _rec_name = "name_fase"
    _columns = {
        'name_fase': fields.char(string="Fase", size=50, required=True),
        'proyect_id': fields.many2one('gdc.proyectos', 'Proyecto', required=True),
    }
    
    _order="name_fase"
    
class gdc_tareas(osv.Model):
    _name = "gdc.tareas"
    _rec_name = "name_tarea"
    _columns = {
        'name_tarea': fields.char(string="Tarea", size=50, required=True),
        'fases_id': fields.many2one('gdc.fases', 'Fase', required=True),
    }
    
    _order="name_tarea"
    
class gdc_proyectos(osv.Model):
    _name = "gdc.proyectos"
    _rec_name = "actividad"
    _columns = {
            'codigo': fields.char(string="Codigo", size=20),  
            'actividad': fields.char(string="Actividad", size=64), 
            'cobertura': fields.selection((('Nacional','Nacional'), ('Regional','Regional'), ('Municipal', 'Municipal')),'Cobertura', required=True),
            'priority': fields.selection((('Baja','Baja'), ('Normal','Normal'), ('Alta', 'Alta')),'Prioridad', required=True),
            'estado': fields.selection((('No Definido','No definido'), ('Propuesti','Propuesto'), ('En Planificacion', 'En Planificacion'), ('En Progreso', 'En progreso'), ('Congelado', 'Congelado'), ('Terminado', 'Terminado'), ('Plantilla', 'Plantilla'), ('Archivado', 'Archivado')),'Estado', required=True),
            'progreso': fields.char(string="Progreso", size=20), 
            'date_start': fields.datetime('Fecha estimada de inicio',select=True),
            'date_end': fields.datetime('Fecha estimada de finalizacion',select=True),
            'responsible_id' : fields.many2one('res.users', 'Responsable asignado', required=True),
            'supervisor_id' : fields.many2one('res.company', 'Supervisor', required=True),
            'description': fields.text('Description'),
            'presu_tentativo': fields.integer('Presupuesto Tentativo'),
            'presu_real': fields.integer('Presupuesto Real'),
            'bene_tentativo': fields.integer('Cantidad de beneficiados tentativos'),
            'members': fields.many2many('res.company', 'project_company_rel', 'project_id', 'uid', 'Entes Encargados'),
            'address_id': fields.many2one('res.partner','Lugar', readonly=False, required=True),
            'street': fields.related('address_id','street',type='char',string='Direccion'),
            'street2': fields.related('address_id','street2',type='char',string='Cont. Direccion'),
            'state_id': fields.related('address_id','state_id',type='many2one', relation="res.country.state", string='Estado'),
            'zip': fields.related('address_id','zip',type='char',string='Codigo Postal'),
            'city': fields.related('address_id','city',type='char',string='Ciudad'),
            'country_id': fields.related('address_id', 'country_id', type='many2one', relation='res.country', string='Pais', readonly=False),
            'fases_ids': fields.one2many('gdc.fases', 'proyect_id', string="Fases"),
            'tareas_ids': fields.one2many('gdc.tareas', 'fases_id', string="Tareas"),
    }
    
    _order="actividad"
    
    _defaults = {
            'supervisor_id': 1,
            'codigo': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'gdc.proyectos'),
            'estado': 'No Definido',
            'progreso': '0.0%',
    }

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
