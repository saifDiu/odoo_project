from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    billinhg_partner_id = fields.Many2one('res.partner', compute='compute_some_data')
    order_id = fields.Many2one('sale.order', compute='compute_some_data')
    customer_ref = fields.Char(compute='compute_some_data')

    def compute_some_data(self):
        for record in self:
            if record.picking_type_code == 'outgoing':
                order_id = self.env['sale.order'].search([('name', '=', record.origin)])
                if order_id:
                    record.billinhg_partner_id = order_id.partner_invoice_id.id
                    record.customer_ref = order_id.client_order_ref
                    record.order_id = order_id.id
            else:
                record.billinhg_partner_id = False
                record.customer_ref = False
                record.order_id = False