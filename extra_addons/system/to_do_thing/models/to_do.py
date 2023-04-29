# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ToDo(models.Model):
    _name = 'my.todo'

    name = fields.Char(string='Name')
    state = fields.Selection([('todo', 'ToDo'),
                              ('progress', 'In progress'),
                              ('done', 'Done')],
                             string='State')


