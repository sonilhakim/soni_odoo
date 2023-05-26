#-*- coding: utf-8 -*-

{
    "name": "GSP - Financial Report Dashboard",
    "version": "1.0", 
    "depends": [
        'base',
        'mail',
        "account",
        "account_accountant",
        "account_reports",
    ],
    "author": "SLH [vitraining.com]",
    "category": "Utility",
    "website": "http://vitraining.com",
    "images": [],
    "price": "10",
    "license": "OPL-1",
    "currency": "IDR",
    "summary": "This is the module for Financial Report Dashboard",
    "description": """

Information
======================================================================

* created menus
* created objects
* created views
* logics

""",
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/type.xml",
        "view/finance_report_dashboard_type.xml",
        "view/finance_report_dashboard.xml",
        # "view/report_line.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
}