# -*- coding: utf-8 -*-
{
    'name': "vit_so_attach_po",

    'summary': """
        Attachment PO Customer""",

    'description': """
        Attachment PO Customer in SO form view.
    """,

    'author': "vitraining.com",
    'website': "http://vitraining.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'sale',],

    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order_view.xml',
    ],
    
}