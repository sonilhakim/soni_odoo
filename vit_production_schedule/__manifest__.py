# -*- coding: utf-8 -*-
{
    'name': "Jadwal Pelaksanaan Produksi",

    'summary': """
        Manage Pelaksanaan Produksi""",

    'description': """
        Manage Pelaksanaan Produksi
    """,

    'author': "SLH@vitraining.com",
    'website': "http://www.vitraining.com",
    'images': ['static/description/icon.png'],

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','vit_marketing','mail','vit_ppic','vit_marketing_sph_garmen'],

    # always loaded
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/pelaksanaan_production_line.xml',
        'data/sequence_masterdata.xml',
        'data/vit.masterdata.jpp.csv',
    ],
}