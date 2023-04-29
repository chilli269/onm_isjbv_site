# -*- coding: utf-8 -*-
{
    'name': 'ToDoShka',
    'version': '15.0.0.1',
    'category': 'project',
    'summary': 'To Do something management system',
    'description': """
    """,
    'author': 'Odoo Evangelist',
    'depends': [
        'base'
        ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/cancel_contract_wizard_views.xml',
        'views/to_do.xml',
        ],
    'installable': True,
    'auto_install': False,
}
