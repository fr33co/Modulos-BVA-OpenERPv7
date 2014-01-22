# -*- coding: utf-8 -*-

import time
import random
from time import gmtime, strftime
from openerp.osv import osv, fields
from datetime import datetime, timedelta

#Clase Solicitud de reparacion de Canaima
class solicitud_soporte(osv.Model):
    _name = "solicitud.soporte"
    _order = 'c_solicitud'
    _rec_name = 'c_solicitud'

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
        'status': fields.selection((('Revisar','Revisar'),('Atendiendo','Atendiendo'),('Reparada','Reparada'), ('Remitida','Remitida'), ('Entregada','Entregada')),'Status', required=True, readonly=True),
        'nombre' : fields.char(string="Nombre", size=25, required=True),
        'apellido' : fields.char(string="Apellido", size=25, required=True),
        't_educ': fields.many2one('solicitud.tipo.edu', 'Tipo de educación', required=True),
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
        'telefono' : fields.char(string="Teléfono", size=11, required=True),	
        'correo' : fields.char(string="Correo Electronico", size=30),
        'pais_r' : fields.many2one('res.country', 'Pais', required=True),
        'estado_r' : fields.many2one('res.country.state', 'Estado', required=True),
        'municipio_r' : fields.many2one('res.country.municipality', 'Municipio', required=True),
        'parroquia_r' : fields.many2one('res.country.parish', 'Parroquia', required=True),
        'direccion_r' : fields.text(string="Dirección", required=True),
        'institucion' : fields.many2one('res.company', 'Institución', required=True, readonly=True),
        'tecnico' : fields.many2one('res.users', 'Técnico Encargado:', required=False),
        'descripcion_tecnico' : fields.text(string="Descripción del Técnico", required=False),
        }
        
    _defaults = {
        'f_solicitud': lambda *a: time.strftime("%d/%m/%Y"),
        'c_solicitud': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'solicitud.soporte'),
        'status': 'Revisar',
        'pais': 240,
        'pais_r': 240,
        'user_register': lambda s, cr, uid, c: uid,
        'institucion': lambda s, cr, uid, c: s.pool.get('res.company')._company_default_get(cr, uid, 'res.users', context=c),
    }     
