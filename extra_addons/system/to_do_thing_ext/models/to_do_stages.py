# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ToDoStage(models.Model):
    _name = 'my.todo.stages'

    name = fields.Char(string='Name')
