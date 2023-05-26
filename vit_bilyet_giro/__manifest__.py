# -*- coding: utf-8 -*-
{
    'name': "Vit Bilyet Giro",

    'summary': """
        Giro and Bilyet""",

    'description': """\

        Features
        ======================================================================

        * mencatat data cek dan giro yg dikeluarkan atau diterima perusahaan untuk membayar hutang atau pelunasan piutang
        * created menu:
            * Accounting / Giro / Giro
        * created object
            * vit.vit_bilyet_giro
        * created views
            * giro
            * invoice
        * logic:
            * user mencatat giro dan mengalokasikan ke invoice-invoice yg hendak di bayar
            * user bisa lihat daftar giro yg jatuh tempo per hari
            * jika dicek ke rek bank, giro tersebut sdh clearing maka user klik tombol clearing
            * system akan membuat invoice payment sesuai alokasi pada giro


        Special thanks to Mr Tiongsin for the business logics :)

    """,

    'author': "akhmad.daniel@gmail.com,richardangga51@gmail.com",
    'category': "Accounting",
    'website': "http://www.vitraining.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'version': '0.4',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        # 'sequence/sequence.xml',
        # 'views/templates.xml',
        'views/invoice.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}   