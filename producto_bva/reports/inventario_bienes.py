#-*- coding: utf-8 -*-

import time

from openerp.report import report_sxw

class inventario_bienes(report_sxw.rml_parse):
    def __init__(self, cr, uid, stock_inventory, context=None):
        super(order, self).__init__(cr, uid, stock.inventory, context=context)
        self.localcontext.update({
            'time': time, 
        })

report_sxw.report_sxw('report.inventario', 'stock_inventory', 'addons/producto_bva/reports/inventario_bienes.rml', parser=inventario_bienes)