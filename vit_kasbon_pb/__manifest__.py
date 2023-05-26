#-*- coding: utf-8 -*-

{
	"name": "vit_kasbon_pb",
	"version": "1.0", 
	"depends": [
		'base','account','hr','stock','payment','vit_report_invoice_custom',
	],
	"author": "SLH [vitraining.com]",
	"category": "Utility",
	"website": "http://vitraining.com",
	"images": ["static/description/images/main_screenshot.jpg"],
	"price": "10",
	"license": "OPL-1",
	"currency": "USD",
	"summary": "Addons untuk mengakomodir kasbon karyawan",
	"description": """

Information
======================================================================

* created menus
* created objects
* created views
* logics

""",
	"data": [
		"security/groups.xml",
		"security/ir.model.access.csv",
		"view/menu.xml",
		"view/payment.xml",
		"view/kasbon_pb.xml",
		"data/sequence_kasbon_pb.xml",
		"data/product_kasbon_pb.xml",
		"view/karyawan.xml", #inherited
		# "view/departemen.xml", #inherited
		"view/product.xml", #inherited
		"view/invoice.xml", #inherited
		# "report/kasbon_pb.xml",
	],
	"installable": True,
	"auto_install": False,
	"application": True,
}