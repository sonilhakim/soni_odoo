{
	"name": "Persediaan",
	"version": "1.0", 
	"depends": [
		"base",
		"stock",
		"board",
		"account",
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
		"view/menu_view.xml",
		"view/menu_aset.xml",
	],
	"installable": True,
	"auto_install": False,
    "application": True,
}