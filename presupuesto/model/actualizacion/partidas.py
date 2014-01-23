#-*- coding:utf-8 -*-
###############################################################################################
#
# Clase para crear las partidas presupuestarias  del modulo de presupuesto 
#
###############################################################################################
from openerp.osv import osv, fields
import re
class Partidas(osv.Model):

    """
     Crear el objeto 'presupuesto.partidas'
    """
    _name = "presupuesto.partidas"

    """
        Ordenar por codigo y llamar la descripcion
    """
    _order='codigo'
    _rec_name='descripcion'

    """
        Declaracion de las Columnas para el xmly la base de datos
    """
    _columns = {
        # many2one para llamar el mismo combo list de esta clase  
        'id_partida' : fields.many2one('presupuesto.partidas','Padre:',ondelete='cascade'),
        'codigo' : fields.char(string="Codigo:",size=13, required=True),
        'descripcion' : fields.text(string="Descripcion:",size=300, required=True),

    }

     # Validar una unica clave por cada codigo de la partida
    _sql_constraints = [
        ('UNICA','unique(codigo)', 'El Codigo de la partida ya se encuentra registrado'),
    ]

    def _check_codigo_accion(self, cr, uid, ids, context=None):
        """
        Constraints para validar que que el codigo de la accion
        sea en formato 00-00-00  
        """
        for codigo in self.read(cr, uid, ids, ['codigo'], context=context): 
            patron = re.compile('^[0-9]{1}\.[0-9]{2}\.[0-9]{2}\.[0-9]{2}\.[0-9]{2}$') 
            if not re.match(patron, codigo['codigo']):
                    return False
        return True

    _constraints = [
        (_check_codigo_accion, 'Error! El Codigo de la partida no es correcto!',['Codigo de Accion']),
    ]