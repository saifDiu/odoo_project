# -*- coding: utf-8 -*-

from odoo import fields, models


class ReverseCharge(models.Model):
    _name = "reverse.charge"
    _description = "Reverse Charge"

    partner_id = fields.Many2one('res.partner', 'Partner')
    inv_id = fields.Many2one('account.move', 'Invoice')
    charge_amount = fields.Float('Charge Amount')
    date = fields.Date('Invoice Date')
