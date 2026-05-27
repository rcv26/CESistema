# -*- coding: utf-8 -*-
{
    'name': "Sistema de Control Electoral - Call Center",

    'summary': """
        Modulo de call center para confirmar delegados
        """,

    'description': """
        Modulo de call center para confirmar delegados
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','ce_base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/delegado_view.xml',
        'views/llamada_view.xml',
        'wizard/call_delegado_view.xml',
        'views/menu.xml',
    ],
}
