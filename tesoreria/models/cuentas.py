# -*- coding: utf-8 -*-

import time # Necesario para las funciones de Fecha

from datetime import date

from openerp.osv import osv, fields

class Bancos(osv.Model):
	#~ _name = "tesoreria.cuenta"
	
	#~ _order = "cuenta"
	
	#~ _rec_name = "cuenta"
	
	_inherit = "res.partner.bank"
	
	#Método para generar el código de las cuentas de la institución
	def generar_codigo(self, cr, uid, ids, banco, context=None):
		values = {}
		
		#Obtención del código del banco
		modelo_bancos = self.pool.get('res.bank')
		
		regs_bancos = modelo_bancos.browse(cr, uid, banco, context=context)
		
		cod_banco = regs_bancos.bic
			
		print cod_banco
		
		
		#Generación del numerador 
		cr.execute('SELECT count(*) as num_cnt FROM res_partner_bank WHERE bank ='+str(banco))
		num_cnt = cr.fetchone()[0]
		
		print num_cnt
		
		cod_cuenta = cod_banco	
		#if num_cnt > 0:
		cod_cuenta = cod_cuenta + str(num_cnt+1).zfill(3)
		#else:
			#cod_cuenta = cod_cuenta + str(num_cnt+1).zfill(3)
		
		
		#Actualización del campo de código
		values.update({
			'codigo' : cod_cuenta
		})
		
		return {'value':values}

	_columns = {
		'codigo': fields.char(string = "Código", required = False),
		#~ 'tipo_banco': fields.many2one("res.bank", "Tipo de Banco", required = True, help="Seleccione el banco"),
		#~ 'cuenta' : fields.char(string="Nro de Cuenta Bancaria", help="Ingrese la cuenta", required = True),
		#~ 'tipo' : fields.selection((('ahorro','Ahorro'),('corriente','Corriente')), "Tipo de Cuenta", required = True),
		#~ 'descripcion' : fields.char(string="Descripción de la Cuenta", required = False),
		#~ 'estatus' : fields.selection((('activa','Activa'),('inactiva','Inactiva')), "Estado de la Cuenta", required = True),
		#~ 'fecha_apertura' : fields.date(string="Fecha de Apertura", required = False),
		#~ 'saldo_ini' : fields.float(string="Saldo Inicial", required = False),
		#~ 'saldo_act' : fields.float(string="Saldo Actual", required = False),
		#~ 'sucursal' : fields.char(string="Sucursal", required = False),
		#~ 'ciudad' : fields.char(string="Ciudad", required = False),
	}

	#NO BORRAR, ES UNA GUÍA...
	#~ _sql_constraints = [
	    #~ ('cedula_familiar_unique',#cedula_becado_unique
	     #~ 'UNIQUE(cedula_familiar)',#cedula_becado
	     #~ 'Disculpe el familiar ya existe'),#Disculpe el Registro ya existe
	#~ ]
	
	_defaults = {
		'country_id' : 240,
		'state_id' : 55,
	}




