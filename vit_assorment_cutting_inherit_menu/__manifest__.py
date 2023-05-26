#-*- coding: utf-8 -*-

{
	"name": "Menu Assortment Cutting Inherit",
	"version": "1.0", 
	"depends": [
		'base','mrp','vit_marketing_po_garmen','vit_merchandise_garment','vit_pengukuran',
		'vit_pengukuran_karyawan_inherit','vit_import_pengukuran','vit_mrp_production_lot_list',
	],
	"author": "SLH [vitraining.com]",
	"category": "Utility",
	"website": "http://vitraining.com",
	"images": ["static/description/images/main_screenshot.jpg"],
	"price": "10",
	"license": "OPL-1",
	"currency": "USD",
	"summary": "Modul menu & print out Assortment Cutting di EDP & Manufacturing.",
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
		# "wizard/assortment_x.xml",
		"view/menu.xml",
	],
	"installable": True,
	"auto_install": False,
	"application": False,
}