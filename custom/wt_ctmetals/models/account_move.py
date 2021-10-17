# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import datetime


class AccountMove(models.Model):
    _inherit = "account.move"

    project_id = fields.Many2one(comodel_name='project.project', string='Project')
    vat_tax = fields.Monetary('DRC VAT', compute='_compute_vat_tax')
    partner_vat_to_hmrc = fields.Boolean(string='Partner VAT to DRC', related="partner_id.vat_to_hmrc")
    
    def action_post(self):
        res = super(AccountMove, self).action_post()
        if self.vat_tax > 0.0:
            self.env['reverse.charge'].create({
                'partner_id': self.partner_id.id,
                'inv_id': self.id,
                'charge_amount': self.vat_tax,
                'date': self.invoice_date,
            })
        return res

    @api.depends('line_ids', 'line_ids.vat_tax_ids')
    def _compute_vat_tax(self):
        for move in self:
            amount = 0.0
            for line in move.line_ids:
                for tx in line.vat_tax_ids:
                    amount += line.price_subtotal * (tx.amount/100)
            move.vat_tax = amount


class AccountMoveline(models.Model):
    _inherit = 'account.move.line'

    vat_tax_ids = fields.Many2many('account.tax', 'account_move_line_vat_tax_rel', 'line_id', 
        string="DRC VAT",
        check_company=True, help="Taxes that apply on the base amount")
