#-*- coding: utf-8 -*-

{
	"name": "Print Out Sticker Polybag",
	"version": "1.4", 
	"depends": [
		'base','vit_pengukuran','vit_pengukuran_karyawan_inherit','vit_import_pengukuran','vit_packing_list','vit_mrp_finished_move_inherit','vit_package_scan',
	],
	"author": "SLH [vitraining.com]",
	"category": "Utility",
	"website": "http://vitraining.com",
	"images": ["static/description/images/main_screenshot.jpg"],
	"price": "10",
	"license": "OPL-1",
	"currency": "USD",
	"summary": "Modul Print Out Sticker Polybag",
	"description": """

Information
======================================================================

* created menus
* created objects
* created views
* logics

""",
	"data": [
		# "security/ir.model.access.csv",
		"wizard/sticker_polybag_lot_wizard.xml",
		"wizard/list_sticker_polybag_wizard.xml",
		"wizard/report_package_wizard.xml",
		"view/package.xml",
		"report/paperformat.xml",
		"report/template.xml",
		"report/sticker_polybag.xml",
		"report/sticker_polybag_lot.xml",
		"report/sticker_polybag_lot_filter.xml",
		"report/list_sticker_polybag.xml",
		"report/list_sticker_polybag_report.xml",
		"report/report_sticker_karton.xml",
	],
	"installable": True,
	"auto_install": False,
	"application": True,
}