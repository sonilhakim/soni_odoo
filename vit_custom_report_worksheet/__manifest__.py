# -*- coding: utf-8 -*-
{
    'name': "vit_custom_report_worksheet",

    'summary': """
        Print Out PDF Worksheet""",

    'description': """
        Print Out PDF Worksheet
    """,

    'author': "Soni LH <Vitraining>",
    'website': "http://www.vitraining.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','mrp','vit_merchandise_garment','vit_mrp_finished_move_inherit'],

    # always loaded
    'data': [
        'wizard/report_worksheet_wizard.xml',
        'views/views.xml',
        'report/template.xml',
        'report/worksheet.xml',
    ],
}