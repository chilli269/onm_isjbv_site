# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _, SUPERUSER_ID


class ToDoCheckListTags(models.Model):
    _name = 'todo.checklist.tags'
    _description = 'Todo Checklist Tags'

    name = fields.Char(string="Name")

