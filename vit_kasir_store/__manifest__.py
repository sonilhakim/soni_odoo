#-*- coding: utf-8 -*-

{
	"name": "Vit Kasir Store",
	"version": "1.5", 
	"depends": [
		'base',
		'stock',
		'product',
		'barcodes',
		'vit_marketing_po_garmen',
		'vit_workorder_lot',
		'vit_sticker_polybag',
		'vit_pengukuran',
		'vit_pengukuran_karyawan_inherit',
	],
	"author": "SLH[vitraining.com]",
	"category": "Utility",
	"website": "http://vitraining.com",
	"images": ["static/description/images/main_screenshot.jpg"],
	"license": "OPL-1",
	"currency": "IDR",
	"summary": "This module to dokumen store activity and swap barcode data of lot/serial number",
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
		# "wizard/sticker_polybag_wizard.xml",
		"view/vit_kasir_store.xml",
		"view/stock_production_lot.xml",
		# "report/paperformat.xml",
		# "report/sticker_polybag_ks.xml",
		"view/packing_list_store.xml",
		"view/picking_type.xml",
	],
	"installable": True,
	"auto_install": False,
	"application": True,
}