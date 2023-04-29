# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ToDoExt(models.Model):
    _inherit = 'my.todo'

    stage_id = fields.Many2one('my.todo.stages')


