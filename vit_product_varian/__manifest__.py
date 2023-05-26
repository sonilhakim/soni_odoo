# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Product Varian in Template',
    'version': '1.0',
    'category': 'Product',
    'summary': 'Add product variant tab in product template',
    'description': """
        Add product variant tab in product template
    """,
    'author': "Vitraining [Soni Lukman Hakim]",
    'website': "http://www.vitraining.com",
    'depends': ["base",
		"stock",
		"product",
		"vit_product_konversi",
		"vit_po_discount_bertingkat",
	],
    'data': [
        "view/product_template.xml",
		"view/product_product.xml",
    ],
    'installable': True,
    'auto_install': False,
}