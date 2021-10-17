from odoo import models, fields, api


class ResCompany(models.Model):
	
	_inherit = 'res.company'

	html_color = fields.Char(
		string="Background Color"
	, default="#875A7B")
	background_image = fields.Binary(string='Background Image')

	bg_selection = fields.Selection(
		[('bg_color', 'Color'),('bg_image', 'Image'),], 
		string="Select Background", default="bg_color")
	navbar_bg_color = fields.Char(
		string="Navbar Background Color"
	, default="#875A7B")

	@api.onchange('bg_selection')
	def onchange_bg_selection(self):
		if self.bg_selection == 'bg_image':
			self.html_color = False
		else:
			self.background_image = False
