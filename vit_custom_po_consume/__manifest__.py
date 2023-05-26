#-*- coding: utf-8 -*-

{
	"name": "Vit Custom Field in Picking and Purchase",
	"version": "1.0", 
	"depends": [
		'base',
		'stock',
		'purchase',
		'purchase_requisition',
		'mrp',
		'vit_package',
		'vit_custom_report_delivery_slip',
		'vit_merchandise_garment',
		'vit_purchase_request_modif',
	],
	"author": "SLH[vitraining.com]",
	"category": "Utility",
	"website": "http://vitraining.com",
	"images": ["static/description/images/main_screenshot.jpg"],
	"license": "OPL-1",
	"currency": "IDR",
	"summary": "This module add custom field in Picking and Purchase",
	"description": """

Information
======================================================================

* created menus
* created objects
* created views
* logics

""",
	"data": [
		"view/picking.xml",
		"view/purchase.xml",
	],
	"installable": True,
	"auto_install": False,
	"application": False,
}