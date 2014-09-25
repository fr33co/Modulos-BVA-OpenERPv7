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
    'name': 'Bienes Nacionales GBA',
    'version': '1.1',
    'author': 'Marcel Arcuri',
    'category': 'Almacenes',
    'depends': ['base','product', 'stock'],
    'description': """

    """,
    'data': [
        ################# Vista de los formularios de: BIENES NACIONALES ###
        'view/bienes/bienes_nacionales.xml',
        'view/bienes/inventario_bva.xml',
        'view/bienes/categoria_bienes.xml',
        'view/bienes/movimientos_bva.xml',
        

        ############################# DATA #################################
        'data/clasificacion_data2.xml',
        'data/ubicaciones_data.xml',
        #'security/groups.xml',
        #'security/ir.model.access.csv',
        #'data/desincorporaciones_data.xml',
        #'data/incorporaciones_data.xml',
        
        'view/configuraciones.xml',
       
        #'view/desincorporaciones.xml',
    ],
    'css': [ 'static/src/css/style.css' ],
    'test': [
      
    ],
    'installable': True,
    'auto_install': False,
 
}