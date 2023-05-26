# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2017 vitraining.com
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
#
##############################################################################

{
    "name": "MRP QTY Produced",
    "version": "1.0",
    "author" : "SLH/vitraining.com",
    "website": "www.vitraining.com",
    "description": """
    
Functionalities:
 - Cek dan Update Qty Produced Work Order


Find our other interesting modules that can make your life easier:
https://www.odoo.com/apps/modules/browse?search=vitraining
        
        
    """,

    "category": "Manufacturing",
    "depends": [
        "mrp",
        "stock",
        "product",
        "vit_mrp_cost",
        "vit_workorder_lot",
    ],

    "data": [],
    "active": False,
    "installable": True,
}

