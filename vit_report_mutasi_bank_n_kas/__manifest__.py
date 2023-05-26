# -*- coding: utf-8 -*-
{
    'name': "Report Mutasi Bank/Kas",

    'summary': """
        Print Report Mutasi Bank/Kas in PDF""",

    'description': """
        Menampilkan menu untuk print Report Mutasi Bank/Kas dalam format PDF.
    """,

    'author': "SLH[vitraining.com]",
    'website': "http://www.vitraining.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','vit_penagihan_faktur'],

    'data': [
        'security/ir.model.access.csv',
        'wizard/report_data.xml',
        'report/template.xml',
        'report/paperformat.xml',
        'report/mutasi_bank_kas.xml',
        # 'wizard/kas.xml',
    ],
    
}