# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2022 Odoo IT now <http://www.odooitnow.com/>
#
##############################################################################

from odoo import models, fields, api, _, registry
from collections import defaultdict
from odoo.exceptions import AccessError, Warning


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    directory_id = fields.Many2one('ir.attachment.directory', string="Directory",
                                   ondelete='restrict')
    document_type = fields.Selection([
        ('portal', 'Portal'),
        ('normal', 'User')],
        string='Document Type', copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner')
    user_ids = fields.Many2many('res.users', string="Users",
                                help="If you select users, then it will visible only to selected users.")
    document_tags = fields.Many2many('document.tag', column1='document_id',
                                      column2='document_tag_id', string='Tags')

    @api.model
    def check(self, mode, values=None):
        """ Overwrite: Restricts the access to an ir.attachment, according to referred mode """
        if self.env.is_superuser():
            return True
        # Always require an internal user (aka, employee) to access to a attachment
        if not (self.env.is_admin() or self.env.user.has_group('base.group_user') \
            or self.env.user.has_group('base.group_portal')):
            raise AccessError(_("Sorry, you are not allowed to access this document."))
        # collect the records to check (by model)
        model_ids = defaultdict(set)            # {model_name: set(ids)}
        if self:
            # DLE P173: `test_01_portal_attachment`
            self.env['ir.attachment'].flush(['res_model', 'res_id', 'create_uid', 'public', 'res_field'])
            self._cr.execute('SELECT res_model, res_id, create_uid, public, res_field FROM ir_attachment WHERE id IN %s', [tuple(self.ids)])
            for res_model, res_id, create_uid, public, res_field in self._cr.fetchall():
                if public and mode == 'read':
                    continue
                if not self.env.is_system() and res_field:
                    raise AccessError(_("Sorry, you are not allowed to access this document."))
                if not (res_model and res_id):
                    continue
                model_ids[res_model].add(res_id)
        if values and values.get('res_model') and values.get('res_id'):
            model_ids[values['res_model']].add(values['res_id'])

        # check access rights on the records
        for res_model, res_ids in model_ids.items():
            # ignore attachments that are not attached to a resource anymore
            # when checking access rights (resource was deleted but attachment
            # was not)
            if res_model not in self.env:
                continue
            if res_model == 'res.users' and len(res_ids) == 1 and self.env.uid == list(res_ids)[0]:
                # by default a user cannot write on itself, despite the list of writeable fields
                # e.g. in the case of a user inserting an image into his image signature
                # we need to bypass this check which would needlessly throw us away
                continue
            records = self.env[res_model].browse(res_ids).exists()
            # For related models, check if we can write to the model, as unlinking
            # and creating attachments can be seen as an update to the model
            access_mode = 'write' if mode in ('create', 'unlink') else mode
            records.check_access_rights(access_mode)
            records.check_access_rule(access_mode)
