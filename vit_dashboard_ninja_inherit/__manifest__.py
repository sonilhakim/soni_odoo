{
	"name": "dashboard ninja inherit",
	"version": "1.0", 
	"depends": [
		"base",
		"ks_dashboard_ninja",
		"base_setup",
	], 
	"author": "vitraining", 
	"category": "Dashboard",
	"description": """\

Manage
======================================================================
Add new tabel under SO template for signature:
* Created By
* Validated By
* Received by


""",
	"data": [
		"view/template.xml",
		# "view/dasbor_temp.xml",
	],
	"qweb": [
        "static/src/xml/dasbor_template.xml",
    ],
	"installable": True,
	"auto_install": False,
}