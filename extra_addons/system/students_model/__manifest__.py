# -*- coding: utf-8 -*-
{
    'name': 'Stundents',
    'version': '1',
    'category': 'project',
    'summary': 'Students Module',
    'description': """
    """,
    'author': 'Mihnea',
    'depends': [
        'base',
        'schools_model',
        ],
    'data': [
        'security/ir.model.access.csv',
        'views/students_db.xml',
        ],
    'installable': True,
    'auto_install': False,
}
