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

#############
# Proyectos #
#############

class gdc_proyectos(osv.Model):
    """
    Modelo para gestionar las actividades
    """
    _name = "gdc.proyectos"
    _rec_name = "actividad"
    _order="actividad"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
  
  
    def on_change_address_id(self, cr, uid, ids, address_id, context=None):
        """
        Onchange para traer toda la informacion de la direccion
        """
        values = {}
        if not address_id:
            return values
        address = self.pool.get('res.partner').browse(cr, uid, address_id, context=context)
        values.update({
            'street' : address.street,
            'street2' : address.street2,
            'city_id' : address.city_id.id,
            'municipality_id' : address.municipality_id.id,
            'parish_id' : address.parish_id.id,
            'zipcode_id' : address.zipcode_id.id,
            'sector_id' : address.sector_id.id,
            'country_id' : address.country_id and address.country_id.id or False,
            'state_id' : address.state_id and address.state_id.id or False,
        })
        print values
        return {'value' : values}
            
    def _compute_days(self, cr, uid, ids, field, arg, context=None):
        """
        Metodo para calcular los dias entre la fecha de inicio y la fecha final
        """
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


    def copy(self, cr, uid, id, default, context=None):
        """
        Metodo para realizar la copia de proyectos
        """
        proyecto = self.browse(cr, uid, id, context=context)
        new_name = "Copia de %s" % proyecto.actividad
        others_count = self.search(cr, uid, [('actividad', '=like', new_name+'%')], count=True, context=context)
        if others_count > 0:
            new_name = "%s (%s)" % (new_name, others_count+1)
        default['actividad'] = new_name
        return super(gdc_proyectos, self).copy(cr, uid, id, default, context=context)


    _columns = {
        'date_created': fields.char('Fecha de Creación',select=True, readonly=True),
        'codigo': fields.char(string="Codigo", size=20),  
        'actividad': fields.char(string="Actividad", size=64, required=True), 
        'cobertura': fields.selection((('Direccionalidad','Direccionalidad'),('Nacional','Nacional'), ('Regional','Regional'), ('Municipal', 'Municipal')),'Cobertura', required=True),
        'priority': fields.selection((('Baja','Baja'), ('Normal','Normal'), ('Alta', 'Alta')),'Prioridad', required=True),
        'tipo_financiamiento': fields.many2one('gdc.fondos', 'Fondos de finaciamiento', required=True),
        'estado': fields.selection((('Borrador','Borrador'), ('Progreso', 'Progreso'), ('Terminado', 'Terminado'), ('Congelado', 'Congelado'), ('Vencido', 'Vencido')),'Estado', required=True),
        'progreso': fields.float(string="Progreso"), 
        'dias_proyecto': fields.function(_compute_days, type='char', string='Cantidad de dias'),
        'date_start': fields.datetime('Fecha inicio',select=True, required=True),
        'date_end': fields.datetime('Fecha final',select=True, required=True),
        'supervisor_id' : fields.many2one('res.company', 'Ente Supervisor', domain=[('category_id.name','ilike','Supervisor')], required=True),        
        'ejecutor_id' : fields.many2one('res.company', 'Ente Ejecutor', required=True),
        'responsible_id' : fields.many2one('res.users', 'Responsable', domain=[('category_id.name','ilike','Responsable')], required=True),
        'description': fields.text('Description', required=True),
        'presu_tentativo': fields.float('Presupuesto Tentativo  (Bs.)', required=True),
        'presu_real': fields.float('Presupuesto Real (Bs.)', required=True),
        'bene_tentativo': fields.integer('Cantidad de beneficiados tentativos', required=True),
        'members_project': fields.many2many('res.company', 'project_company_rel', 'project_id', 'uid', 'Instituciones'),
        
        'address_id': fields.many2one('res.partner','Lugar', readonly=False, required=True, domain=[('category_id.name','ilike','Lugar')]),
        'street': fields.related('address_id','street',type='char',string='Direccion'),
        'street2': fields.related('address_id','street2',type='char',string='Cont. Direccion'),
        'state_id': fields.related('address_id','state_id',type='many2one', relation="res.country.state", string='Estado'),
        'zipcode_id': fields.related('address_id','zipcode_id',type='many2one', relation="res.country.zipcode", string='Zipcode'),
        'city_id': fields.related('address_id','city_id',type='many2one', relation="res.country.city", string='City'),
        'municipality_id': fields.related('address_id','municipality_id',type='many2one', relation="res.country.municipality", string='Municipality'),        
        'parish_id': fields.related('address_id','parish_id',type='many2one', relation="res.country.parish", string='Parish'),
        'sector_id': fields.related('address_id','sector_id',type='many2one', relation="res.country.sector", string='Sector'),
        'country_id': fields.related('address_id', 'country_id', type='many2one', relation='res.country', string='Pais', readonly=False),
        
        'tareas_ids': fields.one2many('gdc.tareas', 'project_id2', string="Tareas"),
        'incidencias_ids': fields.one2many('gdc.incidencias', 'project_id', string="Incidencias"),
        'conclusiones': fields.text('Conclusiones'),
        'acuerdos': fields.text('Acuerdos'),
        'incidencias': fields.text('Incidencias'),
        'adjunto_gaceta': fields.binary('Adjuntar Gaceta digital'),
        'adjunto_gaceta_name': fields.char('Adjuntar Gaceta digital'),
    }
      
        
    def _check_dates_now(self, cr, uid, ids, context=None):
        """
        SQL Constraints para validar que la fecha de inicio 
        debe ser mayor o igual a la fecha de creacion del proyecto
        """
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for leave in self.read(cr, uid, ids, ['date_start'], context=context):
            if leave['date_start']:
                if leave['date_start']:
                    return False
        return True
        
        
    def _check_dates(self, cr, uid, ids, context=None):
        """
        SQL Constraints para validar que La fecha de inicio debe ser 
        menor que la fecha final
        """
        for leave in self.read(cr, uid, ids, ['date_start', 'date_end'], context=context):
            if leave['date_start'] and leave['date_end']:
                if leave['date_start'] > leave['date_end']:
                    return False
        self.send_note(cr, uid, ids, context=context)
        return True
        

    def send_note(self, cr, uid, ids, context=None):
        """
        Envio de notificaciones y correos electronicos al crearse y asignar un proyecto
        """
        # Notificaciones
        for users_not in self.read(cr, uid, ids, ['responsible_id', 'supervisor_id', 'description', 'actividad', 'priority'], context=context):
            responsible = users_not['responsible_id'][0]
            supervisor = users_not['supervisor_id'][0]
            prioridad = users_not['priority']
            supervisor2 = self.pool.get('res.users').read(cr, uid, supervisor, ['partner_id', 'email'], context=context)        
            responsible2 = self.pool.get('res.users').read(cr, uid, responsible, ['partner_id', 'email'], context=context)
            post_vars = {'partner_ids': [(4, supervisor2['partner_id'][0]), (4, responsible2['partner_id'][0])], 'notified_partner_ids': [(supervisor2['partner_id'][0], responsible2['partner_id'][0])]}
            self.message_post(cr, uid, ids, _(users_not['description']),_("Proyecto asignado con prioridad " + prioridad), subtype='mt_comment', context=context, **post_vars)
            # Email
            mail_server_obj = self.pool.get('ir.mail_server')
            mail_message_obj = self.pool.get('mail.message')
            mail_mail_obj = self.pool.get('mail.mail')
            for id in ids:
                mail_message_id = mail_message_obj.create(cr, uid, {'email_from': supervisor2['email'], 'model': 'gdc.proyectos', 'res_id': id, 'subject': users_not['actividad'], 'body': users_not['description']}, context=context)
                mail_server_ids = mail_server_obj.search(cr, uid, [], context=context)
                mail_mail_id = mail_mail_obj.create(cr, uid, {'mail_message_id': mail_message_id, 'mail_server_id': mail_server_ids and mail_server_ids[0], 'state': 'outgoing', 'email_from': supervisor2['email'], 'email_to': responsible2['email'], 'body_html': users_not['description']}, context=context)
                if mail_mail_id:
                    mail_mail_obj.send(cr, uid, [mail_mail_id], context=context)
            return True


    _constraints = [
        (_check_dates_now, 'Error! La fecha de inicio debe ser mayor o igual a la fecha de creacion del proyecto', ['date_start']),
        (_check_dates, 'Error! La fecha de inicio debe ser menor que la fecha final.', ['date_start', 'date_end']),
    ]
    
    
    _sql_constraints = [
        ('actividad_unique','UNIQUE(actividad)','La actividad debe ser unica. Intente copiar el proyecto'),
    ]
    
    
    _defaults = {
            'supervisor_id': lambda s, cr, uid, c: uid,
            'codigo': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'gdc.proyectos'),
            'estado': 'Borrador',
            'progreso': 0.0,
            'date_created': lambda *a: datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'dias_proyecto': 'Aun no asignados. ',
            'priority': 'Baja',
            'adjunto_gaceta_name': 'soporte.pdf',
    }


    def congelar_proyecto(self, cr, uid, ids, context=None):
        result = {}
        records = self.browse(cr, uid, ids, context=context)
        self.write(cr, uid, ids, {'estado': 'Congelado'})
        
        
    def retomar_proyecto(self, cr, uid, ids, context=None):
        result = {}
        records = self.browse(cr, uid, ids, context=context)
        self.write(cr, uid, ids, {'estado': 'Progreso'})
