# -*- coding: utf-8 -*-

import time

from openerp.report import report_sxw

class inventario_materiales(report_sxw.rml_parse):
    def __init__(self, cr, uid, inventario_materiales, context=None):
        super(order, self).__init__(cr, uid, inventario.almacen, context=context)
        self.localcontext.update({
            'time': time, 
        })

report_sxw.report_sxw('report.materiales', 'inventario.almacen', 'addons/producto_bva/reports/inventario_materiales.rml', parser=inventario_materiales)