# -*- coding: utf-8 -*-
{
    'name': "vit_sales_discount",

    'summary': """
        Discount Value in Sales Line""",

    'description': """
        Add discount value field in sales order line
    """,

    'author': "Soni LH <Vitraining>",
    'website': "http://www.vitraining.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account','vit_sale_confirm',],

    # always loaded
    'data': [
        'data/coa.xml',
        'views/sale.xml',
        'views/invoice.xml',
    ],
}