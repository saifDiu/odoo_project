# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectProject(models.Model):
    _inherit = "project.project"

    wso_ids = fields.Many2many('sale.order', compute='_compute_values')
    so_counter = fields.Integer(compute='_compute_values')
    wpo_ids = fields.Many2many('purchase.order', compute='_compute_values')
    po_counter = fields.Integer(compute='_compute_values')

    def action_view_sales(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sale.action_quotations")
        action['domain'] = [('id', 'in', self.wso_ids.ids)]
        return action

    def action_view_purchase(self):
        action = self.env["ir.actions.actions"]._for_xml_id("purchase.purchase_rfq")
        action['domain'] = [('id', 'in', self.wpo_ids.ids)]
        return action

    def _compute_values(self):
        po = self.env['purchase.order']
        po_line= self.env['purchase.order.line']
        for record in self:
            po_exist = po.search([('project_id', '=', record.id)])
            po_exist |= po_line.search([('project_id', '=', record.id)]).mapped('order_id')
            so_exist = self.env['sale.order'].search([('project_id', '=', record.id)])
            record.po_counter = 0
            record.so_counter = 0
            record.wso_ids = None
            record.wpo_ids = None
            if so_exist:
                record.wso_ids = [(6, 0, so_exist.ids)]
                record.so_counter = len(so_exist.ids)
            if po_exist:
                record.wpo_ids = [(6, 0, po_exist.ids)]
                record.po_counter = len(po_exist.ids)

    def unlink(self):
        for record in self:
            po_exist = self.env['purchase.order'].search([('project_id', '=', record.id)])
            so_exist = self.env['sale.order'].search([('project_id', '=', record.id)])
            if so_exist:
                raise ValidationError(_('This Project is link with (Sale Order: %s)', so_exist.mapped('name')))
            if po_exist:
                raise ValidationError(_('This Project is link with (Purchase Order: %s)', po_exist.name('name')))
        return super(ProjectProject, self).unlink()

    @api.model
    def create(self, vals):
        res = super(ProjectProject, self).create(vals)
        self.env['project.task.type'].create({
            'name': 'Finance',
            'project_ids': [(4, res.id)]
            })
        self.env['project.task.type'].create({
            'name': 'Design',
            'project_ids': [(4, res.id)]
            })
        self.env['project.task.type'].create({
            'name': 'Approval',
            'project_ids': [(4, res.id)]
            })
        self.env['project.task.type'].create({
            'name': 'Fabrication',
            'project_ids': [(4, res.id)]
            })
        self.env['project.task.type'].create({
            'name': 'Finish',
            'project_ids': [(4, res.id)]
            })
        self.env['project.task.type'].create({
            'name': 'Delivery',
            'project_ids': [(4, res.id)]
            })
        self.env['project.task.type'].create({
            'name': 'Installation',
            'project_ids': [(4, res.id)]
            })
        return res
