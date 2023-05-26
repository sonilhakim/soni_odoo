# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Attendances Late & Overtime',
    'version': '0.1',
    'category': 'Human Resources',
    'sequence': 88,
    'summary': 'Track employee attendance',
    'description': """
This module aims to manage employee's attendances.
==================================================

Keeps account of the attendances of the employees on the basis of the
actions(Check in/Check out) performed by them.
       """,
    'website': '',
    'depends': ['base','hr', 'hr_contract', 'hr_attendance', 'hr_payroll', 'vit_payroll_tsel', 'vit_overtime_hress'],
    'data': [
        'views/hr_attendance_view.xml',
        'views/hr_overtime.xml',
        'views/hr_contract.xml',
        'data/overtime.xml',
        'data/salary_rule.xml'
    ],
    'css': [
        'static/src/css/vit_late_overtime_attendance.css'
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'qweb': [
    ],
    'application': True,
}
