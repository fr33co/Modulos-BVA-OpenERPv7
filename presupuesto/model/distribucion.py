from openerp.osv import osv, fields
import random
class Estado(osv.Model):
    _name = "presupuesto.distribucion"



    _columns = {
        'proyecto' : fields.many2one('presupuesto.proyecto','Proyecto',ondelete='cascade',required=True),
        'codigo_proyecto' : fields.integer(string="Codigo del Proyecto",size=100, required=True, readonly=True),
        'codigo_accion' : fields.integer(string="Codigo de Accion",size=100, required=True),
        'accion' : fields.many2one('presupuesto.accion','Accion',ondelete='cascade',required=True),
        'partida' : fields.char(string="Partida Presupuestaria",size=100, required=True),
        'descripcion' : fields.text(string="Descripcion",size=300, required=True),
        'monto_pre' : fields.float(string="Monto del Presupesto",size=100, required=True),
        'aceptar' : fields.selection((('1','Ambos'), ('2','Compras'), ('3', 'Servicios')),'Aceptar orden de', required=True),
        'fecha' : fields.date(string="Fecha Apertura", required=True),
        'disponibilidad' : fields.integer(string="Disponibilidad Actual", required=True),
    }


    _order='codigo_proyecto'
    _rec_name='proyecto'

