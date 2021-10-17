# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import datetime, time


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    project_id = fields.Many2one(comodel_name='project.project', string='Project')

    @api.model
    def create(self, vals):
    	res = super(PurchaseOrder, self).create(vals)
    	res.button_confirm()
    	return res

    def _prepare_invoice(self):
        """Prepare the dict of values to create the new invoice for a purchase order.
        """
        invoice_vals = super(PurchaseOrder, self)._prepare_invoice()
        invoice_vals['invoice_date'] = datetime.today().date()
        return invoice_vals


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    project_id = fields.Many2one(comodel_name='project.project', string='Project')
