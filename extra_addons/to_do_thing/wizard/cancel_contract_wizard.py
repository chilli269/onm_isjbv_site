# coding=utf-8

from odoo import api, fields, models, _


import logging

_logger = logging.getLogger(__name__)


class SetState(models.TransientModel):
    _name = "my.todo.wizard"

    to_do_id = fields.Many2one('my.todo', string="Active ID" )
    state = fields.Selection([('todo', 'ToDo'),
                              ('progress', 'In progress'),
                              ('done', 'Done')],
                             default='todo',
                             string='State')

    def action_aplay_state(self):
        self.to_do_id.state = self.state
