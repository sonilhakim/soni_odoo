# -*- coding: utf-8 -*-
{
    'name': "Sistem Pengelolaan Kepegawaian",

    'summary': """
        Menu dan group 'Sistem Pengelolaan Kepegawaian' """,

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Anggaran',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','base_setup','vit_univ_common','hr','vit_skp','website','account','auth_oauth',
    'vit_riwayat','hr_payroll','hr_attendance','hr_holidays','vit_overtime_unhan',
    'vit_bkd','vit_kerja_dosen','vit_kerja_dosen_inherit',],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/decimal_cuti.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/vit_pengajuan.xml',
        'views/master_back_office.xml',
        'views/back_office.xml',
        'views/hak_libur.xml',
        'views/master_front_office.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}