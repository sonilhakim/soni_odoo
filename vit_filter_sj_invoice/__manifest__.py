# -*- coding: utf-8 -*-
{
    'name': "Filter SJ Invoice",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Untuk mem-filter auto-complete dari memilih surat jalan yang sudah pernah di-invoice-kan.
    """,

    'author': "Soni LH <Vitraining>",
    'website': "http://www.vitraining.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','stock','vit_invoices','vit_custom_report_delivery_slip',],

    # always loaded
    'data': [
        'views/views.xml',
    ],
}