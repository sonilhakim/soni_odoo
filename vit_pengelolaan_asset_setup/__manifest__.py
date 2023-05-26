{
	"name": "Set up Aset",
	"version": "1.0", 
	"depends": [
		"base",
		"board",
		"analytic",
		"account",
		"stock",
		"vit_cara_pengadaan",
		"base_setup",
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
		"view/view_form.xml",
		"view/menu_set_up.xml",
		"view/res_config_settings_view.xml",
	],
	"installable": True,
	"auto_install": False,
    "application": True,
}