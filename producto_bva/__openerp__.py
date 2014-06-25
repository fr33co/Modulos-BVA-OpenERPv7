# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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


{
    'name': 'Productos BVA',
    'version': '1.1',
    'author': 'OpenERP SA',
    'category': 'Alamacenes',
    'depends': ['base','product', 'stock'],
    'description': """

    """,
    'data': [
        'view/producto_bva.xml',
        'view/inventario_bva.xml',
        'view/categoria_producto.xml',
        'view/almacen.xml',
        'view/configuraciones.xml',
        'view/reportes_menu.xml',
        'view/inventario_almacen.xml',
        'view/desincorporaciones.xml',
        'view/nota_entrega.xml',
        'view/movimientos_bva.xml',
        'view/solicitudes_bva.xml',
        'data/clasificacion_data2.xml',
        'data/ubicaciones_data.xml',
        'data/desincorporaciones_data.xml',
        'data/incorporaciones_data.xml',
        'reports/inventario_materiales.xml',
        'reports/desincorporaciones_bva.xml',
        #'reports/inventario_bienes.xml',
        'reports/nota_entrega.xml',
        'reports/reporte_mov_bva.xml',
    ],
    'css': [ 'static/src/css/style.css' ],
    'test': [
      
    ],
    'installable': True,
    'auto_install': False,
 
}