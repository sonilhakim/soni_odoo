# -*- coding: utf-8 -*-
{
    'name': "vit_purchase_bill",

    'summary': """
        Purchase Discount Value in Vendor Bill""",

    'description': """
        Add purchase discount value in vendor bill
    """,

    'author': "Soni LH <Vitraining>",
    'website': "http://www.vitraining.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','account','vit_po_discount_bertingkat','vit_product_varian','vit_purchase_product_varian'],

    # always loaded
    'data': [
        'views/invoice.xml',
    ],
}