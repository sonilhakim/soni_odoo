# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'vit_po_discount_bertingkat',
    'version': '1.0',
    'category': 'purchase',
    'summary': 'Add custom discount when purchase order',
    'description': """
        Add custom discount when purchase order
    """,
    'author': "Vitraining [Jaya Dianto]",
    'website': "http://www.vitraining.com",
    'depends': ['purchase','stock','base'],
    'data': [
        'views/views.xml',
        # 'views/purchase_form.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
