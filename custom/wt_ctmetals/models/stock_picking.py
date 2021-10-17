# -*- coding: utf-8 -*-

from odoo import fields, models, api


class StockPickingExtended(models.Model):
	_inherit = "stock.picking"

	project_id_ct = fields.Many2one(comodel_name='project.project', string='Project', compute='_compute_project_id')
	digital_signature = fields.Binary(string="Signature")
	image1 = fields.Binary(string="Delivery Image")
	image2 = fields.Binary(string="Image2")
	image3 = fields.Binary(string="Image3")
	receive_by = fields.Char(string="Received By")
	annotation = fields.Text(string="Annotation")
	user_id = fields.Many2one(
        'res.users', 'Responsible', tracking=True,
        domain=[],
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        default=lambda self: self.env.user)
	
	def _compute_project_id(self):
		project_id = None
		source = None
		for picking in self:
			if picking.picking_type_code == 'outgoing':
				source = self.env['sale.order'].search([('name', '=', picking.origin)])
			if picking.picking_type_code == 'incoming':
				source = self.env['purchase.order'].search([('name', '=', picking.origin)])
			if source:
				picking.project_id_ct = source.project_id.id
			else:
				picking.project_id_ct = None
				

