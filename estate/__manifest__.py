# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "estate",
    'version': '1.0',
    'license': 'LGPL-3',
    'depends': ['base'],
    'author': "Author Name",
    'category': 'Estate',
    'description': """
    Description Text
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [],
}
