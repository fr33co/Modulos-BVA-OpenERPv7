import time

from openerp.report import report_sxw

class order(report_sxw.rml_parse):
    def __init__(self, cr, uid, registrar, context=None):
        super(order, self).__init__(cr, uid, registrar, context=context)
        self.localcontext.update({
            'time': time, 
        })

report_sxw.report_sxw('report.salas', 'registrar.order', 'addons/salas/report/reporte_salas.rml', parser=order)