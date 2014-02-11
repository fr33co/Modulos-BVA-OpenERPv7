# -*- coding: utf-8 -*-

import time

from openerp.report import report_sxw

class reporte_solicitud(report_sxw.rml_parse):
    def __init__(self, cr, uid, reporte_solicitud, context=None):
        super(order, self).__init__(cr, uid, reporte.solicitud, context=context)
        self.localcontext.update({
            'time': time, 
        })

report_sxw.report_sxw('report.soporte', 'reporte.solicitud', 'addons/gestion_canaimas/report/reporte_soporte.rml', parser=reporte_solicitud)