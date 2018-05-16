# Copyright 2017-2018 Camptocamp - Simone Orsi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'CMS status message',
    'summary': """Basic status messages for your CMS system""",
    'version': '11.0.1.1.0',
    'license': 'LGPL-3',
    'author': 'Camptocamp, Odoo Community Association (OCA)',
    'depends': [
        'website',
    ],
    'data': [
        'templates/assets.xml',
        'templates/status_message.xml',
    ],
    'installable': True,
}
