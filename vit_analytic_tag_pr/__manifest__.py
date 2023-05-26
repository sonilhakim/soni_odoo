#-*- coding: utf-8 -*-

{
	"name": "Analytic Tag Inquery",
	"version": "1.1", 
	"depends": [
		'base','analytic','product','stock','mrp','account','vit_product_request','vit_marketing_inquery_garmen','vit_marketing_po_garmen','vit_marketing_request','purchase_requisition',
	],
	"author": "SLH [vitraining.com]",
	"category": "Utility",
	"website": "http://vitraining.com",
	"images": ["static/description/images/main_screenshot.jpg"],
	"price": "10",
	"license": "OPL-1",
	"currency": "USD",
	"summary": "Modul Analytic Tag Inquery untuk Purchse Request",
	"description": """

Information
======================================================================

* created menus
* created objects
* created views
* logics

""",
	"data": [
		"view/inquery.xml",
		"view/product_request.xml",
		"view/marketing_po.xml",
		"view/stock_move.xml",
	],
	"installable": True,
	"auto_install": False,
	"application": False,
}