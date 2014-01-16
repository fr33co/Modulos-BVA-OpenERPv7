import time

from openerp.report import report_sxw

class order(report_sxw.rml_parse):
    def __init__(self, cr, uid, solicitar_sala, context=None):
        super(order, self).__init__(cr, uid, solicitar.sala, context=context)
        self.localcontext.update({
            'time': time, 
        })

report_sxw.report_sxw('report.solicitar.sala', 'solicitar.sala', 'addons/salas/report/salas.rml', parser=order)