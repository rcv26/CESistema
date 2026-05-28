# -*- coding: utf-8 -*-
{
    'name': "Sistema de Control Electoral - Base",

    'summary': """
        Requerimientos base para el funcionamiento del Sistema de Control Electoral
        """,

    'description': """
        Requerimientos base para el funcionamiento del Sistema de Control Electoral
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/pre_data_view.xml',
        'views/referencia_view.xml',
        'views/delegado_view.xml',
        'views/provincia_view.xml',
        'views/canton_view.xml',
        'views/parroquia_view.xml',
        'views/zona_view.xml',
        'views/recinto_view.xml',
        'views/junta_view.xml',
        'views/dignidad_view.xml',
        'views/candidato_view.xml',
        'wizard/asignacion_directa_view.xml',
        'wizard/asignacion_directa_recinto_view.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}
