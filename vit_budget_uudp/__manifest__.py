# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2019  Odoo SA  (http://www.vitraining.com)
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
    "name": "Budget Pengajuan Dana/Biaya",
    "version": "0.1",
    "category": "Extra Tools",
    "sequence": 20,
    "author":  "vITraining",
    "website": "www.vitraining.com",
    "license": "AGPL-3",
    "summary": "",
    "description": """

 * Budget Pengajuan dana / biaya / reimberse

    """,
    "depends": [
        "base",
        "om_account_budget",
        "purchase",
        "vit_budget",
        "vit_uudp",
        "vit_uudp_tier_validation",
    ],
    "data": [
        "views/account_budget_views.xml",
        "views/uudp_views.xml",
    ],

    "demo": [
    ],

    "test": [
    ],

    "installable": True,
    "auto_install": False,
    "application": True,
}

