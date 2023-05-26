# -*- coding: utf-8 -*-
{
    'name': "Sistem Perencanaan",

    'summary': """
        Menu dan group 'Sistem Perencanaan' """,

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Anggaran',
    'version': '0.5',

    # any module necessary for this one to work correctly
    'depends': ['base','anggaran','vit_univ_common','auditlog','vit_account_period','vit_rekap_anggaran'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'wizard/export.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}