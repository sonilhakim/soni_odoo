#-*- coding: utf-8 -*-

{
	"name": "Vit Style Description",
	"version": "2.2", 
	"depends": [
		'base','product','purchase','vit_pengukuran',
	],
	"author": "SLH[vitraining.com]",
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
		"security/ir.model.access.csv",
		"view/data_pengukuran.xml",
	],
	"installable": True,
	"auto_install": False,
	"application": False,
}