# -*- coding: utf-8 -*-
{
    'name': "NM - Project Documents Workspace",
    'summary': """
    Centralize the documents attached to the project and it tasks in one sub workspace
    """,
    'author': "Odoo Evangelist",
    'category': 'Documents',
    'version': '15.0.0.1',
    'depends': ['base',
                'documents',
                'documents_project'],
    'data': [
        'views/views.xml'
    ],
    'images':  ["static/description/image.png"],
    'installable': True,
    'auto_install': False,
    'application': False,
}
