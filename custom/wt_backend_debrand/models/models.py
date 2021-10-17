import base64, os
from odoo import fields, models, api, tools
import re
from lxml import etree, html
import logging
_logger = logging.getLogger(__name__)

class ResUser(models.Model):
    _inherit = "res.users"

    notification_type = fields.Selection([
        ('email', 'Handle by Emails'),
        ('inbox', 'Handle in Systems')],
        'Notification', required=True, default='email',
        help="Policy on how to handle Chatter notifications:\n"
             "- Handle by Emails: notifications are sent to your email address\n"
             "- Handle in Systems: notifications appear in your Systems Inbox")

class Company(models.Model):
    _inherit = "res.company"

    def _get_wt_default_favicon(self, original=False):
        script_dir = os.path.dirname(__file__)
        rel_path = "../static/src/img/favicon.png"
        abs_file_path = os.path.join(script_dir, rel_path)
        with open(abs_file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            return encoded_string.decode("utf-8")

class IrDefault(models.Model):
    _inherit = 'ir.default'

    @api.model
    def set_wt_favicon(self, model, field):
        script_dir = os.path.dirname(__file__)
        rel_path = "../static/src/img/favicon.png"
        abs_file_path = os.path.join(script_dir, rel_path)
        with open(abs_file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            self.set('res.config.settings', 'wt_favicon', encoded_string.decode("utf-8"))

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    wt_favicon = fields.Binary(string="Favicon icon")
    r_title = fields.Char(string="Title", default="Warlock")
    r_text = fields.Char(string='Replace Text', default="Warlock")

    @api.model
    def get_debranding_settings(self):
        IrDefault = self.env['ir.default'].sudo()
        wt_favicon = IrDefault.get('res.config.settings', "wt_favicon")
        r_title = IrDefault.get('res.config.settings', "r_title")
        r_text = IrDefault.get('res.config.settings', "r_text")
        return {
            'wt_favicon': wt_favicon,
            'r_title': r_title,
            'r_text': r_text,
        }

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        IrDefault = self.env['ir.default'].sudo()
        IrDefault.set('res.config.settings', "wt_favicon", self.wt_favicon.decode("utf-8"))
        IrDefault.set('res.config.settings', "r_title", self.r_title)
        IrDefault.set('res.config.settings', "r_text", self.r_text)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        IrDefault = self.env['ir.default'].sudo()
        wt_favicon = IrDefault.get('res.config.settings', "wt_favicon")
        r_title = IrDefault.get('res.config.settings', "r_title")
        r_text = IrDefault.get('res.config.settings', "r_text")
        res.update(
            wt_favicon = wt_favicon,
            r_title = r_title,
            r_text = r_text,
        )
        return res

class Channel(models.Model):
    _inherit = 'mail.channel'

    @api.model
    def init_odoobot(self):
        pass

class MailRenderMixin(models.AbstractModel):
    _inherit = "mail.render.mixin"

    def remove_href_odoo(self, value, remove_parent=True, remove_before=False):
        if len(value) < 20:
            return value
        # value can be bytes type; ensure we get a proper string
        if type(value) is bytes:
            value = value.decode()
        has_odoo_link = re.search(r"<a\s(.*)odoo\.com", value, flags=re.IGNORECASE)
        if has_odoo_link:
            tree = etree.HTML(
                value
            )  # html with broken links   tree = etree.fromstring(value) just xml
            odoo_achors = tree.xpath('//a[contains(@href,"odoo.com")]')
            for elem in odoo_achors:
                parent = elem.getparent()
                previous = elem.getprevious()

                if remove_before and not remove_parent and previous:
                    # remove 'using' that is before <a and after </span>
                    bytes_text = etree.tostring(
                        previous, pretty_print=True, method="html"
                    )
                    only_what_is_in_tags = bytes_text[: bytes_text.rfind(b">") + 1]
                    data_formatted = html.fromstring(only_what_is_in_tags)
                    parent.replace(previous, data_formatted)
                if remove_parent and len(parent.getparent()):
                    # anchor <a href odoo has a parent powered by that must be removed
                    parent.getparent().remove(parent)
                else:
                    if parent.tag == "td":  # also here can be powerd by
                        parent.getparent().remove(parent)
                    else:
                        parent.remove(elem)
            value = etree.tostring(tree, pretty_print=True, method="html")
            # etree can return bytes; ensure we get a proper string
            if type(value) is bytes:
                value = value.decode()
        return re.sub("[^(<)(</)]odoo", "", value, flags=re.IGNORECASE)

    @api.model
    def _render_template(
        self,
        template_src,
        model,
        res_ids,
        engine="jinja",
        add_context=None,
        post_process=False,
    ):
        """replace anything that is with odoo in templates
        if is a <a that contains odoo will delete it completly
        original:
         Render the given string on records designed by model / res_ids using
        the given rendering engine. Currently only jinja is supported.

        :param str template_src: template text to render (jinja) or  (qweb)
          this could be cleaned but hey, we are in a rush
        :param str model: model name of records on which we want to perform rendering
        :param list res_ids: list of ids of records (all belonging to same model)
        :param string engine: jinja
        :param post_process: perform rendered str / html post processing (see
          ``_render_template_postprocess``)

        :return dict: {res_id: string of rendered template based on record}"""
        orginal_rendered = super()._render_template(
            template_src,
            model,
            res_ids,
            engine="jinja",
            add_context=None,
            post_process=False,
        )

        for key in res_ids:
            orginal_rendered[key] = self.remove_href_odoo(orginal_rendered[key])

        return orginal_rendered


class MailMail(models.AbstractModel):
    _inherit = "mail.mail"

    # in messages from objects is adding using Odoo that we are going to remove

    @api.model_create_multi
    def create(self, values_list):
        for index, _value in enumerate(values_list):
            values_list[index]["body_html"] = self.env[
                "mail.render.mixin"
            ].remove_href_odoo(
                values_list[index].get("body_html", ""),
                remove_parent=0,
                remove_before=1,
            )

        return super().create(values_list)