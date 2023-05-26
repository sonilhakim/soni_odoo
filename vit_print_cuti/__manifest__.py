#-*- coding: utf-8 -*-

{
	"name": "Print Out Cuti",
	"version": "1.0", 
	"depends": [
		'base','hr','hr_holidays',
	],
	"author": "SLH [vitraining.com]",
	"category": "Utility",
	"website": "http://vitraining.com",
	"images": ["static/description/images/main_screenshot.jpg"],
	"price": "10",
	"license": "OPL-1",
	"currency": "USD",
	"summary": "Modul Print Out pengajuan Cuti",
	"description": """

Information
======================================================================

* created menus
* created objects
* created views
* logics

""",
	"data": [
		"report/paperformat.xml",
		"report/template.xml",
		"report/permohonan_cuti.xml",
	],
	"installable": True,
	"auto_install": False,
	"application": True,
}