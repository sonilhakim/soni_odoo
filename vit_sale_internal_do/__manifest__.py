# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'vit_sale_internal_do',
    'version': '1.0',
    'category': 'sale',
    'summary': 'Create Internal DO from Sale Order',
    'description': """
        Create Internal DO from Sale Order
    """,
    'author': "Vitraining [SLH]",
    'website': "http://www.vitraining.com",
    'depends': ['sale','stock','sale_stock','vit_sale_show_qty','vit_so_attach_po'],
    'data': [
        'views/views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
