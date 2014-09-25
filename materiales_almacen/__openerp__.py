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
    'name': 'Materiales de Almacen GBA',
    'version': '1.1',
    'author': 'Marcel Arcuri',
    'category': 'Almacenes y Suministros',
    'depends': ['base','product', 'stock'],
    'description': """
        Modulo para la gestión de materiales tales como papeleria, limpieza, etc.
    """,
    'data': [
        ################# Vista de los formularios de: ALMACEN #############
        'view/almacen/almacen.xml',
        'view/almacen/inventario_almacen.xml',
        'view/almacen/nota_entrega.xml',
        'view/almacen/solicitudes_materiales.xml',
        ################# Vista de los Reportes ############################
        'view/reportes/reportes_solicitudes.xml',
        'view/reportes/reportes_inventario.xml',
        'view/reportes/reportes_notas_entregas.xml',
        ################## Wizard Resumen ##################################
        'wizard/wizard_resumen_inventario.xml',
        ############################# DATA #################################
        'data/nombre_materiales.xml',
        ################# Grupos de Usuarios y Permisos ####################
        'security/groups.xml',
        'security/ir.model.access.csv',

    ],
    'css': [ 'static/src/css/style.css' ],
    'test': [
      
    ],
    'installable': True,
    'auto_install': False,
 
}