# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError


class IrUiMenuExtended(models.Model):

	_inherit = "ir.ui.menu"

	@api.model
	@tools.ormcache_context('self._uid', 'debug', keys=('lang',))
	def load_menus(self, debug):
		res = super(IrUiMenuExtended,self).load_menus(debug)
		res.update({"navbar_bg_color": self.env.company.navbar_bg_color,
					"company_color": self.env.company.html_color,
					"company_bg_image": self.env.company.background_image,
					"background_selection": self.env.company.bg_selection})
		return res