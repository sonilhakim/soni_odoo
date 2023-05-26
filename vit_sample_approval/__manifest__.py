#-*- coding: utf-8 -*-

{
	"name": "Vit sample approval",
	"version": "1.4", 
	"depends": [
		'base','mrp','stock','product','uom','vit_marketing_po_garmen','vit_merchandise_garment','vit_product_request',
	],
	"author": "SLH [vitraining.com]",
	"category": "Utility",
	"website": "http://vitraining.com",
	"images": ["static/description/images/main_screenshot.jpg"],
	"price": "10",
	"license": "OPL-1",
	"currency": "USD",
	"summary": "This is the Vit sample approval module",
	"description": """

Information
======================================================================

* created menus
* created objects
* created views
* logics

""",
	"data": [
		"data/squence.xml",
		"security/group.xml",
		"security/ir.model.access.csv",
		"wizard/pr_sample.xml",
		"wizard/mo_sample_wizard.xml",
		"view/sample_approval.xml",
		"view/sample_approval_line.xml",
		"view/production.xml",
		"view/product_request.xml",
	],
	"installable": True,
	"auto_install": False,
	"application": True,
}