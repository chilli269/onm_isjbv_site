# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProjectTaskSeqEv(models.Model):
    _inherit = 'project.task'

    sequence_name = fields.Char("Sequence", readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('sequence_name', _('New')) == _('New'):
            vals['sequence_name'] = self.env['ir.sequence'].next_by_code('project.tasks') or _('New')
        res = super(ProjectTaskSeqEv, self).create(vals)
        return res

