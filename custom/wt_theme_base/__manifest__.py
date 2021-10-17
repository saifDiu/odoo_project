# -*- coding: utf-8 -*-
# Part of Warlock Technologies Pvt. Ltd. See COPYRIGHT & LICENSE files for full copyright and licensing details.

{
    "name": "wt Enterprise Theme",
    "version": "14.0.0.1",
    "category": "",
    "summary": "wt enterprise theme base",
    "description": """
    design home decoration online.
    """,
    "author": "Warlock Technologies Pvt Ltd.",
    "website": "http://warlocktechnologies.com",
    "support": "support@warlocktechnologies.com",
    "depends": ['web','base'],
    "data": [
        'views/assets.xml',
        'views/login.xml',
        'views/res_company.xml',
        ],
    'qweb': [
        "static/src/xml/*.xml",
        ],
    "images": [],
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "OPL-1",
}
