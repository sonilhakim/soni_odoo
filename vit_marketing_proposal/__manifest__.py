#-*- coding: utf-8 -*-

{
	"name": "Vit marketing proposal",
	"version": "1.6", 
	"depends": [
		'base','stock','uom','vit_marketing','vit_marketing_inherit','vit_marketing_inquery_garmen'
	],
	"author": "SLH [vitraining.com]",
	"category": "Utility",
	"website": "http://vitraining.com",
	"images": ["static/description/images/main_screenshot.jpg"],
	"price": "10",
	"license": "OPL-1",
	"currency": "USD",
	"summary": "This is the Vit marketing proposal module",
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
		"view/marketing_proposal.xml",
		"report/marketing_proposal_report.xml",
	],
	"installable": True,
	"auto_install": False,
	"application": True,
}