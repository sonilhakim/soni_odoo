#-*- coding: utf-8 -*-

{
	"name": "data_buruh",
	"version": "1.0", 
	"depends": [
		'base','account',
	],
	"author": "SLH [vitraining.com]",
	"category": "Utility",
	"website": "http://vitraining.com",
	"images": ["static/description/images/main_screenshot.jpg"],
	"price": "10",
	"license": "OPL-1",
	"currency": "USD",
	"summary": "Mengakomodir Data Buruh per hari dan rekapan upah buruh.",
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
		"data/data.xml",
		"view/menu.xml",
		"view/data_buruh.xml",
		"view/res_partner.xml", #inherited
		# "view/daftar_buruh.xml",
		"view/rekap_data_buruh.xml",
		# "view/rekap_daftar_buruh.xml",
		"report/data_buruh.xml",
		"report/rekap_data_buruh.xml",
	],
	"installable": True,
	"auto_install": False,
	"application": True,
}