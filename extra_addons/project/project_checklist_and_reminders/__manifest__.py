# -*- coding: utf-8 -*-
{
    'name': "Checklist and Reminders",
    'author': 'Odoo Evangelist',
    'category': 'Employees',
    'summary': """ To Do List for Projects, Tasks, Subtasks, and Personal use """,
    'description': """ 
    """,
    'version': '15.0.0.1',
    'depends': [
        'base',
        'project',
        'hr_attendance',
        'hr_timesheet'
    ],
    'data': [
             'security/ir.model.access.csv',
             'views/todo_checklist_view.xml',
             'views/todo_checklist_tags_views.xml',
            ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
