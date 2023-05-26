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
    "name": "Posisi Dana",
    "version": "0.1",
    "category": "Extra Tools",
    "sequence": 30,
    "author":  "SLH[VITraining]",
    "website": "www.vitraining.com",
    "license": "AGPL-3",
    "summary": "",
    "description": """
    
    * Menu Worksheet
    """,
    "depends": [
        "base",
        "account",
        "purchase",
        "vit_marketing_po_garmen",
        "ks_dashboard_ninja",
    ],
    "data": [
        # "security/group.xml",
        "security/ir.model.access.csv",
        "wizard/posisi_dana_wizard.xml",
        "views/partner.xml",
        "views/view.xml",
    ],


    "demo": [
    ],

    "test": [
    ],

    "installable": True,
    "auto_install": False,
    "application": True,

}