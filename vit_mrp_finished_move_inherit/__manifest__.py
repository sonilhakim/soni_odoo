#-*- coding: utf-8 -*-

{
	"name": "Vit MRP Finished Move Inherit",
	"version": "1.2", 
	"depends": [
		'base','product','stock','mrp','vit_merchandise_garment','vit_pengukuran_karyawan_inherit','vit_mrp_production_lot_list','vit_summary_produce_routing','vit_workorder','vit_workorder_lot',
	],
	"author": "SLH[vitraining.com]",
	"category": "Utility",
	"website": "http://vitraining.com",
	"images": ["static/description/images/main_screenshot.jpg"],
	"price": "10",
	"license": "OPL-1",
	"currency": "USD",
	"summary": "This is the Modification of MRP Finished Move",
	"description": """

Information
======================================================================

* created menus
* created objects
* created views
* logics

""",
	"data": [
		# "data/squence.xml",
		"security/ir.model.access.csv",
		"view/menu.xml",
	],
	"installable": True,
	"auto_install": False,
	"application": True,
}