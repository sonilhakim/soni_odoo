{
	"name": "Pengadaan Pemakaian Aset",
	"version": "1.1", 
	"depends": [
		"base",
		"board",
		"purchase",
		"purchase_requisition",
		"stock",
		"mrp",
		"account",
		"maintenance",
		"hr_maintenance",
		"vit_pemakaian_aset",
		"vit_univ_common",
		"anggaran",
		"mail",
	],
	"author": "vitraining.com",
	"category": "Accounting",
	'website': 'http://www.vitraining.com',
	'images': ['static/description/images/main_screenshot.jpg'],
	'price': '10',
	'license': 'OPL-1',
	'currency': 'USD',
	'summary': 'This is the summary',
	"description": """\

Manage
======================================================================

* this is my academic information system module
* created menu:
* created object
* created views
* logic:

""",
	"data": [
		# "security/groups.xml",
		"security/ir.model.access.csv",
		"view/menu_view.xml",
		"view/menu_pengadaan_pemakaian.xml",
		"view/purchase.xml",
		"view/equipment.xml",
		"view/asset.xml",
	],
	"installable": True,
	"auto_install": False,
    "application": True,
}