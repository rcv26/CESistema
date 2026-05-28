# -*- coding: utf-8 -*-
{
    'name': "Odoo Chat Edit/Delete",
    'summary': """The Odoo App provides the feature of editing and deleting an already sent message in Odoo Chat. """,
    'description': """	-Odoo Chat
            -Chat
            -Chat Edit
            -Chat Delete
            -Discussion Edit
            -Discussion Delete
            -Message Edit
            -Message Delete 
            -Chat App
            -Odoo Chat App
            -Odoo Chat Edit App
            -Odoo Chat Delete App
            chat integration apps, 
            odoo chat modules, 
            POS chat box, 
            Odoo chat box, 
            odoo chat apps, 
            odoo live chat module, 
            odoo chat extension, 
            manage odoo chats, 
                """,
    'author': "Ksolves India Ltd.",
    'website': "https://store.ksolves.com/",
    'category': 'Tools',
    'version': '14.0.1.0.2',
    'license': 'LGPL-3',
    'currency': 'EUR',
    'support': 'sales@ksolves.com',
    'live_test_url': 'https://www.youtube.com/watch?v=KpU4IcpDR5Y',
    'depends': ['base', 'mail', 'base_setup', 'web'],
    'data': [
        'views/ks_assets.xml',
        'views/ks_inherited_res_config.xml',
    ],
    'qweb': ['static/src/xml/ks_inherited_mail_config.xml'],
    'images': [
        'static/description/Odoo-chat_Edit_Delete_V14.jpg',
    ],
}
