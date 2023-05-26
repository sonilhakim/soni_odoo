# -*- coding: utf-8 -*-
# Part of Kiran Infosoft. See LICENSE file for full copyright and licensing details.

{
    'name': 'Report Rekap Inventory',
    'summary': 'Report Rekap Inventory',
    'description': """
Report Rekap Inventory
""",
    'author': "SLH",
    "website": "http://www.vitraining.com",
    'category': 'Stock',
    'version': '1.0',
    'license': 'Other proprietary',
    'price': 0.0,
    'currency': 'IDR',
    'images': [],
    'depends': [
        'web','stock','mrp','purchase',
    ],
    'data': [
        'wizard/rekap_bkb_wizard_view.xml',
        'wizard/rekap_btb_wizard_view.xml',
        'wizard/rekap_stock_acc_wizard.xml',
        'wizard/jadwal_persiapan_material_wizard.xml',
        'wizard/form_stock_wizard.xml',
        'wizard/rekap_mutasi_wizard.xml',
        'report/rekap_bkb_view.xml',
        'report/rekap_btb_view.xml',
        'report/rekap_stock_acc.xml',
        'report/jadwal_persiapan_material_view.xml',
        'report/form_stock_view.xml',
        'report/mutasi_stock.xml',
        'views/report_action.xml',
    ],
    'installable': True,
}
