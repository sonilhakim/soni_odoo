# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2021  Odoo SA  (http://www.vitraining.com)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Purchase Request FOB",
    "version": "1.0",
    "category": "Extra Tools",
    "sequence": 20,
    "author":  "SLH[VITraining]",
    "website": "www.vitraining.com",
    "license": "AGPL-3",
    "summary": "",
    "description": """
    
    * Menu Job Order
    * Menu Material List
    * Menu Material List
    * Menu Worksheet
    * Menu Material Card
    * Jadwal Pelaksanaan Order
    """,
    "depends": [
        "base",
        "mrp",
        "product",
        "stock",
        "vit_product_request",
        "vit_marketing_po_garmen",
        "vit_marketing_request",
        "vit_merchandise_garment",
        "vit_mrp_production_lot_list",
    ],
    "data": [
        "wizard/product_request_fob.xml",
        "views/po_lines.xml",
        "views/product_request.xml",
    ],


    "demo": [
    ],

    "test": [
    ],

    "installable": True,
    "auto_install": False,
    "application": True,

}