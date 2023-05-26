#-*- coding: utf-8 -*-

{
	"name": "GSP - COMPANY KEY PERFORMANCE INDICATOR",
	"version": "1.0", 
	"depends": [
		'base',
		'mail',
	],
	"author": "SLH [vitraining.com]",
	"category": "Utility",
	"website": "http://vitraining.com",
	"images": ["static/description/images/main_screenshot.jpg"],
	"price": "10",
	"license": "OPL-1",
	"currency": "USD",
	"summary": "This is the KEY PERFORMANCE INDICATOR module",
	"description": """

Information
======================================================================

* created menus
* created objects
* created views
* logics

""",
	"data": [
		"security/security.xml",
		"security/ir.model.access.csv",
		"data/squence.xml",
		"view/menu.xml",
		"view/kpi_gsp.xml",
		"view/kpi_aspek.xml",
		"view/kpi_lines.xml",
		"report/kpi_gsp.xml",
	],
	"installable": True,
	"auto_install": False,
	"application": True,
}