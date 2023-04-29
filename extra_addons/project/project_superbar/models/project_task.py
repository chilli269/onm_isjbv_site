# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = 'project.task'

    user_id = fields.Many2one('res.users', string='Responsible')
