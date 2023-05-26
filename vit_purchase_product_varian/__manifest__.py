# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Purchase Product Varian',
    'version': '1.0',
    'category': 'Purchase',
    'summary': 'Add custom field product variant in purchase',
    'description': """
        Add custom field product variant in purchase
    """,
    'author': "Vitraining [Soni Lukman Hakim]",
    'website': "http://www.vitraining.com",
    'depends': ["base",
		"stock",
		"product",
        "purchase",
        "vit_product_konversi",
		"vit_product_varian",
	],
    'data': [
        "view/purchase.xml",
        "view/partner.xml",
        "report/template.xml",
        "report/paper.xml",
        "report/report_custom_purchase.xml",
    ],
    'installable': True,
    'auto_install': False,
}