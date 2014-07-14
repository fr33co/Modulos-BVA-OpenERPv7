# -*- coding: utf-8 -*-

import time

from openerp.report import report_sxw

class Individual(report_sxw.rml_parse):

	def __init__(self, cr, uid, gestion_eventos, context=None):
		super(order, self).__init__(cr, uid, gestion.eventos, context=context)
		self.localcontext.update({
			'time': time,
		})

report_sxw.report_sxw('report.individual', 'gestion.eventos', 'addons/gestion_eventos/individual/individual.rml', parser=Individual)
