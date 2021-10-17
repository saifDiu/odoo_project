{
    "name": "Stock Picking Report",
    "version": "14.0.0.1",
    "category": "stock",
    "summary": "customized stock picking report",
    "description": """
    customized stock picking report
    """,
    "author": "Warlock Technologies Pvt Ltd.",
    "website": "http://warlocktechnologies.com",
    "support": "info@warlocktechnologies.com",
    "depends": ['stock'],
    'data': [
        'views/stock_picking_view.xml',
        'report/stockpicking_report.xml',
        'report/stockpicking_templates.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
