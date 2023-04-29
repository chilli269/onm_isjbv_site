# -*- coding: utf-8 -*-
{
    'name': 'Auto Sequence on Project Task',
    'version': '15.0.0.1',
    'category': 'Project',
    'summary': 'This app help to create automatic sequence of project task',
    'description': """
    """,
    'author': 'Odoo Evangelist',
    'depends': [
        'project'
        ],
    'data': [
        'data/ir_sequence_data.xml',
        'views/project_task.xml',
        ],
    'installable': True,
    'auto_install': False,
}
