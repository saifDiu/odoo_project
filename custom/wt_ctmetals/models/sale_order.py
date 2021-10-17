# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo import api, fields, models, _
from odoo.exceptions import Warning


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _log_payment_transaction_received(self):
        super(PaymentTransaction, self)._log_payment_transaction_received()
        for trans in self.filtered(lambda t: t.provider not in ('manual', 'transfer')):
            post_message = trans._get_payment_transaction_received_message()
            for so in trans.sale_order_ids:
                if so.customer_limit_check() and self.partner_id.client_type == 'cash':
                    so.update({'state': 'sent'})
                so.message_post(body=post_message)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    project_id = fields.Many2one(comodel_name='project.project', string='Project')
    vat_tax = fields.Monetary('DRC VAT', compute='_amount_all')
    partner_vat_to_hmrc = fields.Boolean(string='Domestic Reverse Charge', related="partner_id.vat_to_hmrc")
    is_credit_limit_exceeded = fields.Boolean(string='Exceeded', compute="_compute_credit_limit")

    @api.depends('amount_total')
    def _compute_credit_limit(self):
        for rec in self:
            rec.is_credit_limit_exceeded = False
            if rec.customer_limit_check() and rec.partner_id.client_type == 'credit' and rec.state in ['draft', 'sent']:
                rec.is_credit_limit_exceeded = True

    def customer_limit_check(self):
        total_amount = 0
        if self.partner_id.client_type == 'credit':
            # orders_amount_residual = sum(self.env['sale.order'].search([('partner_id', '=', self.partner_id.id), ('state', '=', 'sale')]).invoice_ids.filtered(lambda x: x.amount_residual != 0).mapped('amount_residual'))
            orders = self.env['sale.order'].search([('partner_id', '=', self.partner_id.id), ('state', '=', 'sale')])
            orders_amount_residual = self.amount_total + sum(orders.filtered(lambda l: not l.invoice_ids).mapped('amount_total')) + \
                                    sum(orders.filtered(lambda l: l.invoice_ids).invoice_ids.filtered(lambda x: x.amount_residual != 0).mapped('amount_residual'))
            if orders_amount_residual < self.partner_id.credit_limit or self.env.user.has_group('wt_ctmetals.group_is_eligible_to_confirm_so'):
                return False
            return True
        else:
            return True
        
    def action_confirm(self):
        if self.customer_limit_check() and self.partner_id.client_type == 'credit':
            raise Warning(_('credit limit has exceeded! You can not confirm this order.'))
        return super(SaleOrder, self).action_confirm()

    # override existing computation
    @api.depends('order_line.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = vat_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
                for tx in line.vat_tax_ids:
                    vat_tax += line.price_subtotal * (tx.amount/100)
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'vat_tax': vat_tax,
                'amount_total': amount_untaxed + amount_tax + vat_tax,
            })

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['project_id'] = self.project_id.id
        return invoice_vals


    def _find_mail_template(self, force_confirmation_template=False):
        template_id = False
        if force_confirmation_template or (self.state == 'sale' and not self.env.context.get('proforma', False)):
            template_id = int(self.env['ir.config_parameter'].sudo().get_param('sale.default_confirmation_template'))
            template_id = self.env['mail.template'].search([('id', '=', template_id)]).id
            if not template_id:
                template_id = self.env['ir.model.data'].xmlid_to_res_id('sale.mail_template_sale_confirmation', raise_if_not_found=False)
        elif self.env.context.get('proforma', True):
            template_id = int(self.env['ir.config_parameter'].sudo().get_param('sale.default_proforma_template'))
            template_id = self.env['mail.template'].search([('id', '=', template_id)]).id
            if not template_id:
                template_id = self.env['ir.model.data'].xmlid_to_res_id('wt_ctmetals.email_template_pro_forma_sale', raise_if_not_found=False)
        if not template_id:
            template_id = self.env['ir.model.data'].xmlid_to_res_id('sale.email_template_edi_sale', raise_if_not_found=False)
        return template_id


class OrderLine(models.Model):
    _inherit = 'sale.order.line'

    vat_tax_ids = fields.Many2many('account.tax', 'sale_order_tax_rel',
        'line_id', string="DRC VAT", context={'active_test': False},
        check_company=True, help="Taxes that apply on the base amount",
        domain=[('type_tax_use','=','sale')])

    @api.onchange('product_id')
    def product_id_change(self):
        res = super(OrderLine, self).product_id_change()
        if self.order_id.partner_vat_to_hmrc:
            self.tax_id = False
            line = self.with_company(self.company_id)
            fpos = line.order_id.fiscal_position_id or line.order_id.fiscal_position_id.get_fiscal_position(line.order_partner_id.id)
            taxes = line.product_id.taxes_id.filtered(lambda t: t.company_id == line.env.company)
            line.vat_tax_ids = fpos.map_tax(taxes, line.product_id, line.order_id.partner_shipping_id)
        return res


    def _prepare_invoice_line(self, **optional_values):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        :param optional_values: any parameter that should be added to the returned invoice line
        """
        self.ensure_one()
        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'discount': self.discount,
            'price_unit': self.price_unit,
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'vat_tax_ids': [(6, 0, self.vat_tax_ids.ids)],
            'analytic_account_id': self.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'sale_line_ids': [(4, self.id)],
        }
        if optional_values:
            res.update(optional_values)
        if self.display_type:
            res['account_id'] = False
        return res


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, name, amount, so_line):
        invoice_vals = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(order, name, amount, so_line)
        invoice_vals['project_id'] = order.project_id
        return invoice_vals