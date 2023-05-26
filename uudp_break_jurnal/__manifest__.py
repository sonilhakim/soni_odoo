# -*- coding: utf-8 -*-
{
    'name': "uudp break jurnal",

    'summary': """
        Breakdown Jurnal UUDP Penyelesaian
        """,

    'description': """
        Menambah kolom analytic account di uudp
    """,

    'author': "sonilukmanhakim",
    'website': "",
    'category': 'Akunting',
    'version': '1.0',
    'depends': ['vit_uudp',
                'analytic',
                'vit_uudp_analytic_account',
    ],

    'data': [
        'views/uudp.xml',
    ],
    "demo": [],
    "installable": True,
    "auto_install": False,
    "application": True,
}