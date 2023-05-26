# -*- coding: utf-8 -*-
{
    'name': "vit_address",

    'summary': """
        Invoice Address & Shipping Address""",

    'description': """
        Invoice Address & Shipping Address
    """,

    'author': "yusup[vITraining.com]",
    'website': "http://www.vITraining.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    
}