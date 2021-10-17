# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    vat_to_hmrc = fields.Boolean(string='DRC VAT')
    credit_limit = fields.Float('Credit Limit')

    client_type = fields.Selection([
        ('cash', 'Cash Client'),
        ('credit', 'Credit Client'),
    ], required=True, default='credit')

    