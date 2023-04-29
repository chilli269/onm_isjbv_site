# -*- coding: utf-8 -*-
{
    'name': "System Bugs Management",
    'summary': """System Bugs Management""",
    'description': """
        System Bugs Management. Error control and bug fixes in the Odoo Open source platform
    """,
    'version': '15.0.0.1',
    'category': 'Tools',
    'author': "ToDOO, Odoo Evangelist",
    'depends': [
        'base',
        'project',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/management_bug_security.xml',
        'views/management_bug.xml',
        'data/bugs_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
