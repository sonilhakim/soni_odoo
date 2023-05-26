#-*- coding: utf-8 -*-

{
	"name": "Vit SPK Pengukuran",
	"version": "1.5", 
	"depends": [
		'base','stock','product','uom','vit_marketing','vit_marketing_inherit','vit_marketing_po_garmen',
	],
	"author": "SLH [vitraining.com]",
	"category": "Utility",
	"website": "http://vitraining.com",
	"images": ["static/description/images/main_screenshot.jpg"],
	"price": "10",
	"license": "OPL-1",
	"currency": "USD",
	"summary": "This is the Vit spk pengukuran module",
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
		"view/spk_pengukuran.xml",
		"report/spk_pengukuran_report.xml",
	],
	"installable": True,
	"auto_install": False,
	"application": True,
}