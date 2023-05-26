# -*- coding: utf-8 -*-
{
    'name': "vit_sales_payment_kas",

    'summary': """
        Create Payment untuk Sales dengan pembayaran Kas""",

    'description': """
        Create Payment untuk Sales dengan pembayaran Kas
    """,

    'author': "Soni LH <Vitraining>",
    'website': "http://www.vitraining.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account','sale_management','vit_sales_discount'],

    # always loaded
    'data': [
        'report/paperformat.xml',
        'report/template.xml',
        'report/struk.xml',
        'wizard/make_invoice_payment.xml',
        'views/sale.xml',
        'views/invoice.xml',
    ],
}