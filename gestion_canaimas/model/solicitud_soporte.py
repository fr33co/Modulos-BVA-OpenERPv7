# -*- coding: utf-8 -*-

import time
import random
from time import gmtime, strftime
from openerp.osv import osv, fields
from datetime import datetime, timedelta

# Clase Solicitud de reparacion de Canaima
class solicitud_soporte(osv.Model):

    #  Nombre del objeto
    _name = "solicitud.soporte"

    #  Ordenar por codigo de solicitud y de ser llamado por otro  objeto muestre codigo de solicitud
    _order = 'c_solicitud'
    _rec_name = 'c_solicitud'

    # Acciones de cada uno de los botones de la barra de estado de solicitud
    def action_atendiendo(self, cr, uid, ids, context = None):
        return self.write(cr, uid, ids, {'status':'Atendiendo'}, context=context)

    def action_remitir(self, cr, uid, ids, context = None):
        return self.write(cr, uid, ids, {'status':'Remitir'}, context=context)

    def action_confirmado(self, cr, uid, ids, context = None):
        return self.write(cr, uid, ids, {'status':'Reparada'}, context=context)

    def action_listo(self, cr, uid, ids, context = None):
        return self.write(cr, uid, ids, {'status':'Entregada'}, context=context)

    def action_devuelta(self, cr, uid, ids, context = None):
        return self.write(cr, uid, ids, {'status':'Devuelta'}, context=context)

# """
# Metodo que genera el codigo se solicitud donde se busca el ultimo valor encontrado en la BD
# y se le suma 1.
# """
    def _get_last_id(self, cr, uid, ids, context = None):

        sfl_id       = self.pool.get('solicitud.soporte')
        srch_id      = sfl_id.search(cr,uid,[])
        rd_id        = sfl_id.read(cr, uid, srch_id, context=context)
        if rd_id:
            id_documento = rd_id[-1]['c_solicitud']
            c_solicitud = id_documento[3:]
            last_id      = c_solicitud.lstrip('0')
            str_number   = str(int(last_id) + 1)
            last_id      = str_number.rjust(6,'0')
            codigo      = 'SSC'+last_id
        else :
            str_number = '1'
            last_id      = str_number.rjust(6,'0')
            codigo      = 'SSC'+last_id
        return codigo

    _columns = {
        'c_solicitud' : fields.char(string="Código de Solicitud", size=255, readonly=True, required=True),
        'user_register': fields.many2one('res.users', 'Registrado por:', readonly=True),
        'f_solicitud': fields.char('Fecha de Solicitud', readonly=True, required=True),
        'f_entrega': fields.date('Fecha de Entrega', required=True),
        'modelo' : fields.many2one('solicitud.modelo', string="Modelo", required=True),
        'serial' : fields.char(string="Serial", required=True),
        'descripcion' : fields.text(string="Descripción del Problema", required=True),
        'canaimita' : fields.boolean('Portatil'),
        'cargador' : fields.boolean('Cargador'),
        'bateria' : fields.boolean('Bateria'),
        'caja' : fields.boolean('Caja'),
        'contrato' : fields.boolean('Contrato'),
        'otros' : fields.boolean('Otros'),
        'status': fields.selection((('Atendiendo','Atendiendo'),('Remitir','Remitir'), ('Reparada','Reparada'), ('Entregada','Entregada'),('Devuelta','Devuelta')),'Status', required=True, readonly=True),
        'nombre' : fields.char(string="Nombre", size=25, required=True),
        'apellido' : fields.char(string="Apellido", size=25, required=True),
        't_educ': fields.many2one('solicitud.tipo.edu', 'Tipo de Nivel', required=True),
        'grado' : fields.many2one('solicitud.grado', string="Grado de estudio", required=True),
        'escuela' : fields.char(string="Escuela", size=50, required=True),
        'pais' : fields.many2one('res.country', 'Pais', required=True),
        'estado' : fields.many2one('res.country.state', 'Estado', required=True),
        'municipio' : fields.many2one('res.country.municipality', 'Municipio', required=True),
        'parroquia' : fields.many2one('res.country.parish', 'Parroquia', required=True),
        'direccion_i' : fields.text(string="Dirección Escuela", required=True),
        'nombre_r' : fields.char(string="Nombre Representante", size=25, required=True),
        'apellido_r' : fields.char(string="Apellido Representante", size=25, required=True),
        'cedula' : fields.char(string="Cédula", size=10, required=True),
        'telefono' : fields.char(string="Teléfono 1", size=11, required=True),	
        'telefono2' : fields.char(string="Teléfono 2", size=11, required=False),    
        'correo' : fields.char(string="Correo Electronico", size=30),
        'pais_r' : fields.many2one('res.country', 'Pais', required=True),
        'estado_r' : fields.many2one('res.country.state', 'Estado', required=True),
        'municipio_r' : fields.many2one('res.country.municipality', 'Municipio', required=True),
        'parroquia_r' : fields.many2one('res.country.parish', 'Parroquia', required=True),
        'direccion_r' : fields.text(string="Dirección", required=True),
        'solucion' : fields.text(string="Solución", required=False, readonly=True),  
        #'grafico' : fields.function(_grafica_modelos, type='integer', string='Conteo por modelo', store=True),
        'grafico': fields.integer('Modelos', track_visibility='always'),
        }
        
    """
    Por defecto declaramos: 
            -El formato del campo de fecha de solicitud por dia, mes y año
            -El estatus de la solicitud inicie como Atendiendo
            -El campo Registrado cargue el nombre del usuario logeado
            -El pais por defecto vamos a filtrar.
    """
        
    _defaults = {
        'f_solicitud': lambda *a: time.strftime("%d/%m/%Y"),
        'c_solicitud': _get_last_id,
        'status': 'Atendiendo',
        'pais': 240,
        'pais_r': 240,
        'user_register': lambda s, cr, uid, c: uid,
        'grafico': 1,
    }     
