{
	"name": "Modul Aset",
	"version": "1.0", 
	"depends": [
		"base",
		"board",
		"account",
		"stock",
		"vit_asset_bmn",
		"vit_referensi_aset",
		"vit_referensi_aset_inherit",
		"vit_product_request",
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
		"security/ir.model.access.csv",
		"view/view_form.xml",
		"view/menu_aset.xml",
		
	],
	"installable": True,
	"auto_install": False,
    "application": True,
}