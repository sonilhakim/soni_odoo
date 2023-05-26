# -*- coding: utf-8 -*-
{
    'name': "vit_custom_report_picking",
    'summary': "Custom report picking_operations",
    'description': "Custom report picking_operations",
    'author': "slh@gmail.com",
    'website': "http://www.vitraining.com",
    'category': 'Uncategorized',
    'version': '1.1',
    'depends': ['stock','base',],
    'data': [
        'views/stock_picking.xml',
        'report/paperformat.xml',
        'report/template.xml',
        'report/template_int_do.xml',
        'report/delivery_slip.xml',
        'report/picking_operations.xml',
    ],
}