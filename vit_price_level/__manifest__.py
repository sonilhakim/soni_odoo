# -*- coding: utf-8 -*-
{
    'name': "vit_price_level",

    'summary': """
        Price Level""",

    'description': """
        Level Harga barang berdasarkan kategori Customer.
    """,

    'author': "vitraining.com",
    'website': "http://vitraining.com",
    'category': 'Sales',
    'version': '0.1',
    'depends': ['base', 'sale', 'product', 'vit_product_varian'],

    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'views/price_level.xml',
        'views/view.xml',
    ],
    
}