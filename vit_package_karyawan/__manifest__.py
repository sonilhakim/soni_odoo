# -*- coding: utf-8 -*-
{
    'name': "vit_package_karyawan",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "SLH",
    'website': "http://www.vitraining.com",
    'category': 'Stock',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['stock','vit_pengukuran_karyawan_inherit','vit_package'],

    # always loaded
    'data': [
        'views/stock_move_line.xml',
    ],
}