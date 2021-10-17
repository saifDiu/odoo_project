# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    so_email = fields.Char(string='Sales Email')
    po_email = fields.Char(string='Purchase Email')
    sp_email = fields.Char(string='Stock Picking Email')
    invoice_email = fields.Char(string='Invoice Email')
    rfq_po_email = fields.Char(string='Purchase Production Email')
    utr = fields.Char(string='UTR')
    bank_details = fields.Char(string='Bank Details')
    sort_code = fields.Char(string='Sort Code')
    account_no = fields.Char(string='account_no')
    delivery_confirm_email = fields.Char(string='Delivery Confirm Email')
