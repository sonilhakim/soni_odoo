#-*- coding: utf-8 -*-

{
	"name": "Gedung dan Ruang",
	"version": "1.0", 
	"depends": [
		'base','hr','om_account_asset','vit_asset','vit_univ_common',
	],
	"author": "SLH [vitraining.com]",
	"category": "Utility",
	"website": "http://vitraining.com",
	"images": ["static/description/images/main_screenshot.jpg"],
	"price": "10",
	"license": "OPL-1",
	"currency": "USD",
	"summary": "This is the Gedung dan Ruang module generated by StarUML Odoo Generator Pro Version",
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
		"view/vit_gedung.xml",
		# "view/accountasset.xml",
		# "view/users.xml",
		"view/vit_ruang.xml",
		# "view/unit_kerja.xml",
		"view/guna_ruang.xml",
		"report/vit_gedung.xml",
		"report/accountasset.xml",
		"report/users.xml",
		"report/vit_ruang.xml",
		"report/unit_kerja.xml",
		"report/guna_ruang.xml",
	],
	"installable": True,
	"auto_install": False,
	"application": True,
}