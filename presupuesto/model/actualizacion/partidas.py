#-*- coding:utf-8 -*-
###############################################################################################
#
# Clase para crear las partidas presupuestarias  del modulo de presupuesto 
#
###############################################################################################
from openerp.osv import osv, fields
import random
class Partidas(osv.Model):

    """
     Crear el objeto 'presupuesto.partidas'
    """
    _name = "presupuesto.partidas"

    """
        Ordenar por codigo y llamar la descripcion
    """
    _order    ='codigo'
    _rec_name ='descripcion'

    """
        Declaracion de las Columnas para el xmly la base de datos
    """
    _columns = {
        # many2one para llamar el mismo combo list de esta clase  
        'id_partida' : fields.many2one('presupuesto.partidas','Padre:',ondelete='cascade'),
        'codigo' : fields.char(string="Codigo:",size=20, required=True),
        'descripcion' : fields.text(string="Descripcion:",size=300, required=True),

    }

    _sql_constraints = [
        ('codigo_unique', 'UNIQUE(codigo)', 'El Codigo de la Partida ya se encuantra registrado!')
    ]
    

