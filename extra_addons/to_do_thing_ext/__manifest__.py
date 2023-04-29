# -*- coding: utf-8 -*-
{
    'name': 'ToDoShka Ext',
    'version': '15.0.0.1',
    'category': 'project',
    'summary': 'To Do something management system Ext',
    'description': """
    """,
    'author': 'Odoo Evangelist',
    'depends': [
        'to_do_thing'
        ],
    'data': [
        'security/ir.model.access.csv',
        'views/to_do.xml',
        ],
    'installable': True,
    'auto_install': False,
}
