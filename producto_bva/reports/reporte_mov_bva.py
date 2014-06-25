# -*- coding: utf-8 -*-

import time

from openerp.report import report_sxw

class movimientos_bva(report_sxw.rml_parse):
    def __init__(self, cr, uid, stock_move, context=None):
        super(order, self).__init__(cr, uid, stock.move, context=context)
        self.localcontext.update({
            'time': time, 
        })

report_sxw.report_sxw('report.movimientos', 'stock.move', 'addons/producto_bva/reports/reporte_mov_bva.rml', parser=movimientos_bva)