import jinja2
import json
import os
from xml.etree import ElementTree as ET
import odoo
from odoo import http
from odoo.addons.web.controllers.main import DBNAME_PATTERN, db_monodb,\
    Database as DB

loader = jinja2.PackageLoader('odoo.addons.wt_backend_debrand',
                              "views")
env = jinja2.Environment(loader=loader, autoescape=True)
env.filters["json"] = json.dumps


class Database(DB):
    def _render_template(self, **d):
        d.setdefault('manage',True)
        d['insecure'] = odoo.tools.config.verify_admin_password('admin')
        d['list_db'] = odoo.tools.config['list_db']
        d['langs'] = odoo.service.db.exp_list_lang()
        d['countries'] = odoo.service.db.exp_list_countries()
        d['pattern'] = DBNAME_PATTERN
        d['repalce_texts'] = self.get_replace_odoo_datas()
        d['favicon_url'] = self.get_favicon_url()
        # databases list
        d['databases'] = []
        try:
            d['databases'] = http.db_list()
            d['incompatible_databases'] = odoo.service.db.list_db_incompatible(d['databases'])
        except odoo.exceptions.AccessDenied:
            monodb = db_monodb()
            if monodb:
                d['databases'] = [monodb]
        return env.get_template("database_manager.html").render(d)

    def get_replace_odoo_datas(self):
        script_dir = os.path.dirname(__file__)
        rel_path = "../static/src/xml/debrand.xml"
        abs_file_path = os.path.join(script_dir, rel_path)
        root = ET.parse(abs_file_path).getroot()
        title = root.find('span[@id="title"]').text
        r_text = root.find('span[@id="rtitle"]').text
        return {'title': title, 'r_text': r_text}

    def get_favicon_url(self):
        script_dir = os.path.dirname(__file__)
        rel_path = "../static/src/xml/debrand.xml"
        abs_file_path = os.path.join(script_dir, rel_path)
        root = ET.parse(abs_file_path).getroot()
        favicon_url = root.find('span[@id="rfavicon"]').text
        return favicon_url