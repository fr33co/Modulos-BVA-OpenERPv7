# -*- coding: utf-8 -*-

import time

from openerp.report import report_sxw

class desincorporacion_bva(report_sxw.rml_parse):
    def __init__(self, cr, uid, desincorporaciones_bva, context=None):
        super(order, self).__init__(cr, uid, desincorporaciones.bva, context=context)
        self.localcontext.update({
            'time': time, 
        })

report_sxw.report_sxw('report.desincorporaciones', 'desincorporaciones.bva', 'addons/producto_bva/reports/desincorporaciones_bva.rml', parser=desincorporacion_bva)