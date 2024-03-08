# -*- coding: utf-8 -*-
{
    'name': "Peminjaman Buku",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Muhammad Rizky Gaez",
    'website': "https://www.linkedin.com/in/muhammad-rizky-gaez-743022166/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'data/mail_data.xml',
        'views/peminjam_buku_views.xml',
        'views/master_buku_views.xml',
        'views/master_genre_buku_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
