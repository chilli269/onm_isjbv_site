# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2022 Odoo IT now <http://www.odooitnow.com/>
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Directory(models.Model):
    _name = 'ir.attachment.directory'
    _description = "Documents Directory"

    @api.depends('child_directories')
    def _compute_count_directories(self):
        for record in self:
            record.count_directories = len(record.child_directories)

    @api.depends('files')
    def _compute_count_files(self):
        for record in self:
            record.count_files = len(record.files)

    name = fields.Char(string="Name", required=True)
    image = fields.Binary(string="Image")
    is_root_directory = fields.Boolean(string="Root Directory", default=False,
                                       help="Indicates if the directory is a root directory.")
    parent_directory = fields.Many2one('ir.attachment.directory',
                                       string="Parent Directory", ondelete='restrict',
                                       index=True)
    child_directories = fields.One2many('ir.attachment.directory', 'parent_directory',
                                        copy=False, string="Subdirectories")
    parent_left = fields.Integer(string='Left Parent', index=True)
    parent_right = fields.Integer(string='Right Parent', index=True)
    files = fields.One2many('ir.attachment', 'directory_id', copy=False, string="Files")
    count_directories = fields.Integer(compute='_compute_count_directories',
                                       string="Subdirectories Count")
    count_files = fields.Integer(compute='_compute_count_files', string="Files Count")
    directory_tags = fields.Many2many('directory.tag', column1='directory_id',
                                      column2='directory_tag_id', string='Tags')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Directory name already exists !"),
    ]

    def _get_action(self, action_xmlid):
        # TDE TODO check to have one view + custo in methods
        action = self.env.ref(action_xmlid).read()[0]
        if self:
            action['display_name'] = self.name
        return action

    def get_action_attachment_directory(self):
        self.ensure_one()
        action = self._get_action('portal_documents_management.action_attachment_directory_child')
        action['domain'] = [('parent_directory', '=', self.id)]
        return action

    def get_action_directory_documents(self):
        self.ensure_one()
        action = self._get_action('portal_documents_management.action_directory_documents')
        action['domain'] = [('directory_id', '=', self.id)]
        return action

    def unlink(self):
        for directory in self:
            personal_dir = self.env.ref('portal_documents_management.personal_directory')
            shared_dir = self.env.ref('portal_documents_management.shared_directory')
            if directory.id in [personal_dir.id, shared_dir.id]:
                raise UserError(_("Sorry...! you can't delete Personal/Shared directory, you can rename it."))
        return super(Directory, self).unlink()
