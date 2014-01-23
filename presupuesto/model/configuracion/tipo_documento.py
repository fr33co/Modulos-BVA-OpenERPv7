from openerp.osv import osv, fields
import random
class Documento(osv.Model):
    """
     Crear el objeto 'presupuesto.documento'
    """
    _name = "presupuesto.documento"


    _order='id_documento desc'
    _rec_name='documento'

    """
        Declaracion de las Columnas para el xmly la base de datos
    """

    _columns = {
        'id_documento' : fields.char(string="Codigo del Documento:",size=100),
        'siglas' : fields.char(string="Siglas del Documento:",size=6, required=True),
        'documento' : fields.char(string="Tipo de Documento:",size=100, required=True),
        'tipo' : fields.selection((('1','Traspaso/Traslado'), ('2','Creditos Adiconales')),'Tipo', required=True),
    }

    def _get_last_id(self, cr, uid, ids, context = None):
        """
        Metodo para obtener el ultimo id_documento 
        """

        # funcion para obtener los registros de la tabla 'presupuesto.documento'
        sfl_las_id  = self.pool.get('presupuesto.documento')


        # funcion que nos permite saber si la tabla tiene registro segun el criterio de busqueda,
        # la busqueda se realiza con,
        # para obtener todos los registros de la tabla
        srcnt_last_num = sfl_las_id.search_count(cr, uid, [], context=None)

        if srcnt_last_num > 0:

            # la busqueda se realiza con,
            # para obtener todos los registros de la tabla
            # offset inicio de los registro 
            # limit cantdad de registros a obtener
            # order tipo 'ASC' o 'DESC' de orden y columna por el cual ordenar
            srch_id = sfl_las_id.search(cr,uid,[],offset=0,limit=1,order='id_documento desc')

            # funcion que obtiene los registros de que genero el search 
            rd_id   = sfl_las_id.read(cr, uid, srch_id,['id_documento'], context=context)

            # obtener el registro por indice y clave
            id_documento = rd_id[0]['id_documento']

            # funcion para eliminar los '0' a la derecha 
            last_id      = id_documento.lstrip('0')

            # sumar '1' al registro obtenido
            str_number   = str(int(last_id) + 1)

            # agregar '0' a la derecha en este caso son '6' 
            last_id      = str_number.rjust(6,'0')
        else:
            str_number = '1'
            last_id    = str_number.rjust(6,'0')
        return last_id
    _defaults = {
        'id_documento' : _get_last_id
    }