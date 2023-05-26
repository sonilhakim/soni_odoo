#-*- coding: utf-8 -*-

{
	"name": "Vit Purchase Request Modif",
	"version": "2.2", 
	"depends": [
		'base','purchase','vit_product_request',
	],
	"author": "[vitraining.com]",
	"category": "Utility",
	"website": "http://vitraining.com",
	"images": [],
	"price": "10",
	"license": "OPL-1",
	"currency": "USD",
	"summary": "This is the Modification of Vit Product Request",
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
		"security/ir.model.access.csv",
		"view/menu.xml",
		"view/purchase_request.xml",
		"view/purchase_order.xml",
	],
	"installable": True,
	"auto_install": False,
	"application": False,
}