# -*- coding: utf-8 -*-
{
    'name': "vit_elearning",

    'summary': """
        Website Elearning
    """,

    'description': """
    """,

    'author': "Soni Lukman Hakim <vitraining>",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.5',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'website', 'e_learning', 'auth_signup',],

    # always loaded
    'data': [
        'data/menu_data.xml',
        'data/mail_data.xml',
        'views/elearning.xml',
        'views/myaccount.xml',
        'views/header.xml',
        'views/footer.xml',
        'views/kelasonline.xml',
        'views/kelasonlines.xml',
        'views/kelasonline_free.xml',
        'views/kelasonlines_free.xml',
        'views/kelasonline_mentor.xml',
        'views/kelasonlines_mentor.xml',
        'views/seminaronline.xml',
        'views/admission.xml',
        'views/single-courses.xml',
        'views/single-seminar.xml',
        'views/single-courses-lock.xml',
        'views/single-seminar-lock.xml',
        'views/error.xml',
        'views/succes.xml',
        'views/search_page.xml',
        'views/artikel.xml',
        'views/about.xml',
        'views/artikel-detail.xml',
        'views/our-mentor.xml',
        'views/register.xml',
        'views/reset_password.xml',
        # 'data/group.xml',
        # 'security/ir.model.access.csv',
    ],
}