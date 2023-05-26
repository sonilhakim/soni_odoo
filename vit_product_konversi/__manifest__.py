{
	"name": "Konversi Antar Product",
	"version": "1.0", 
	"depends": [
		"base",
		"stock",
		"product",
	], 
	"author": "Soni@Vitraining.com", 
	"category": "Stock",
	"description": """\

Manage
======================================================================
Konversi antar product


""",
	"data": [
		"view/product_konversi.xml",
		"view/product_product.xml",
		"security/ir.model.access.csv",
		"data/ir_sequence.xml",
	],
	"installable": True,
	"auto_install": False,
}