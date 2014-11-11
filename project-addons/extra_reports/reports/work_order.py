# -*- coding: utf-8 -*-

import time

from openerp.report import report_sxw

class work_order(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(work_order, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
			'time': time,
		})
    
report_sxw.report_sxw('report.work_order', 'project.task',
                      'addons/extra_reports/reports/work_order.rml',
                      parser=work_order, header="external")
        
        
        
        