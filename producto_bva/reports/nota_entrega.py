# -*- coding: utf-8 -*-

import time

from openerp.report import report_sxw

class nota_entrega(report_sxw.rml_parse):
    def __init__(self, cr, uid, nota_entrega, context=None):
        super(order, self).__init__(cr, uid, nota.entrega, context=context)
        self.localcontext.update({
            'time': time, 
        })

report_sxw.report_sxw('report.nota.entrega', 'nota.entrega', 'addons/producto_bva/reports/nota_entrega.rml', parser=nota_entrega)