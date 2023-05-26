#-*- coding: utf-8 -*-

{
	"name": "Pengukuran Pakaian",
	"version": "2.6", 
	"depends": [
		'base',
		'product',
		'stock',
		'sale',
		'mrp',
		'vit_spk_pengukuran'
	],
	"author": "vitraining.com",
	"category": "Utility",
	"website": "http://vitraining.com",
	"images": ["static/description/images/main_screenshot.jpg"],

	"summary": "Modul untuk input data pengukuran",
	"description": """

Information
======================================================================

* created menus
* created objects
* created views
* logics

""",
	"data": [
		"data/sequence.xml",
		"data/data.xml",
		"security/group.xml",
		"security/ir.model.access.csv",
		"wizard/add_style.xml",
		"view/menu.xml",
		"view/pengukuran.xml",
		"view/edp.xml",
		"view/divisi_karyawan.xml",
		"view/jabatan_karyawan.xml",
		"view/lokasi_karyawan.xml",
		"view/template_pengukuran.xml",
		"view/data_pengukuran.xml",
		"view/pengukuran_header.xml",
		"view/pengukuran_karyawan.xml",
		"view/spk_pengukuran.xml",
		"view/stock_lot.xml",
		"view/metode_pengukuran.xml",
		"report/pengukuran.xml",
	],
	"installable": True,
	"auto_install": False,
	"application": True,
}