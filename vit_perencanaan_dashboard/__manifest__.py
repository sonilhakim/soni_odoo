# -*- coding: utf-8 -*-
{
    'name': "Sistem Perencanaan Dashboard",

    'summary': """
        Menu dashboard dibawah Sistem Perencanaan""",

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
    'depends': ['base','anggaran','ks_dashboard_ninja','vit_perencanaan'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/dashboard.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}