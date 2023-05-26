# -*- coding: utf-8 -*-
{
    'name': "vit_report_purchase",

    'summary': """
        Report Purchase""",

    'description': """
        Report Purchase
    """,

    'author': "Soni LH [vitraining.com], Hanifah NA [vitraining.com]",
    'website': "http://www.vitraining.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','purchase','purchase_requisition','stock','vit_product_request','report_xlsx','hr',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/menu.xml',
        'wizard/rekap_belanja_cash.xml',
        'wizard/po_thd_btbw.xml',
        'wizard/pembelian_pembayaran_supw.xml',
        'wizard/monitoring_pembelian_blnw.xml',
    ],
    
}