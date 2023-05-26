# -*- coding: utf-8 -*-
{
    'name': "Sistem Pengelolaan Keuangan",

    'summary': """
        Menu dan group 'Sistem Pengelolaan Keuangan' """,

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Anggaran',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','vit_univ_common','account','om_account_accountant','account_reports','account_analytic_default','sale','accounting_pdf_reports'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}