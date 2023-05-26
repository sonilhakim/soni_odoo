# -*- coding: utf-8 -*-
{
    'name': "vit_koversi_product_sales",

    'summary': """
        Konversi Product in Sales Line""",

    'description': """
        Add location field in sales order line,
        Konversi product when confirm sales.
    """,

    'author': "Soni LH <Vitraining>",
    'website': "http://www.vitraining.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','stock','sale_stock','vit_sale_show_qty','vit_sale_confirm','vit_product_konversi',],

    # always loaded
    'data': [
        'views/sale.xml',
    ],
}