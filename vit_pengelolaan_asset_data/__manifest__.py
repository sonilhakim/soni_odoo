{
	"name": "Pendataan Aset",
	"version": "1.0", 
	"depends": [
		"base",
		"board",
		"account",
		"vit_asset",
		"auth_oauth",
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
		"security/groups.xml",
		"security/ir.model.access.csv",
		"view/menu_inventaris.xml",
		"view/menu_pendataan.xml",
		"view/menu_button.xml"
	],
	"installable": True,
	"auto_install": False,
    "application": True,
}