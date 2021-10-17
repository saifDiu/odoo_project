#-*- coding:utf-8 -*-
from odoo import api, models, _


class PaymentReport(models.AbstractModel):
    _name = 'report.wt_ctmetals.report_dms_charges'
    _description = 'Account report without payment lines'  

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['reverse.charge'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'reverse.charge',
            'docs': docs,
        }
