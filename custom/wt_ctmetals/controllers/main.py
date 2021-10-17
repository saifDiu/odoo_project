# -*- coding: utf-8 -*-
import binascii

from odoo import http
from odoo import fields, http, _
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.website.controllers.main import Website
from odoo.addons.sale.controllers.portal import CustomerPortal
import base64


class CustomerPortal(CustomerPortal):
	@http.route(['/delivery'], type='http', auth='public', website=True, method='POST')
	def delivery(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
		values = {}
		picking_id = None
		print()
		partner = request.env.user.partner_id
		picking_ids = request.env['stock.picking'].sudo().search([('picking_type_code', '=', 'outgoing')])
		delivery = picking_ids.sudo().filtered(
			lambda x: x.user_id.partner_id == partner and
			x.state == 'assigned'
		)
		values.update({
			'delivery': delivery,
			'page_name': 'delivery',
		})
		if kw.get('picking_id'):
			picking_id = request.env['stock.picking'].sudo().search([('id', '=', int(kw.get('picking_id')))])
		if kw.get('signature'):
			picking_id.digital_signature = kw.get('signature')
		if kw.get('annotation'):
			picking_id.annotation = kw.get('annotation')
		if kw.get('receive_by'):
			picking_id.receive_by = kw.get('receive_by')
		if kw.get('alpha'):
			image1 = kw.get('alpha').replace('data:image/jpeg;base64,','')
			picking_id.image1 = image1
		if kw.get('bravo'):
			image2 = kw.get('bravo').replace('data:image/jpeg;base64,','')
			picking_id.image2 = image2
		if kw.get('charlie'):
			image3 = kw.get('charlie').replace('data:image/jpeg;base64,','')
			picking_id.image3 = image3
		if picking_id:
			template_id = request.env.ref("wt_ctmetals.email_template_stock_picking")
			template_id.sudo().send_mail(picking_id.id, force_send=True, email_values={'email_to': picking_id.company_id.delivery_confirm_email})
		return request.render('wt_ctmetals.delivery_templ',values)

	@http.route(['/my/orders/<int:order_id>/accept'], type='json', auth="public", website=True)
	def portal_quote_accept(self, order_id, access_token=None, name=None, signature=None):
		# get from query string if not on json param
		access_token = access_token or request.httprequest.args.get('access_token')
		try:
			order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
		except (AccessError, MissingError):
			return {'error': _('Invalid order.')}

		if not order_sudo.has_to_be_signed():
			return {'error': _('The order is not in a state requiring customer signature.')}
		if not signature:
			return {'error': _('Signature is missing.')}

		try:
			order_sudo.write({
				'signed_by': name,
				'signed_on': fields.Datetime.now(),
				'signature': signature,
			})
			request.env.cr.commit()
		except (TypeError, binascii.Error) as e:
			return {'error': _('Invalid signature data.')}

		if not order_sudo.has_to_be_paid():
			# if order_sudo.partner_id.client_type != 'cash':
			order_sudo.action_confirm()
			order_sudo._send_order_confirmation_mail()

		pdf = request.env.ref('sale.action_report_saleorder').sudo()._render_qweb_pdf([order_sudo.id])[0]

		_message_post_helper(
			'sale.order', order_sudo.id, _('Order signed by %s') % (name,),
			attachments=[('%s.pdf' % order_sudo.name, pdf)],
			**({'token': access_token} if access_token else {}))

		query_string = '&message=sign_ok'
		if order_sudo.has_to_be_paid(True):
			query_string += '#allow_payment=yes'
		return {
			'force_refresh': True,
			'redirect_url': order_sudo.get_portal_url(query_string=query_string),
		}
