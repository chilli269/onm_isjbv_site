# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2022 Odoo IT now <http://www.odooitnow.com/>
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class DirectoryTag(models.Model):
    _description = 'Directory Tags'
    _name = 'directory.tag'
    _order = 'parent_left, name'
    _parent_store = True
    _parent_order = 'name'

    name = fields.Char(string='Tag Name', required=True, translate=True)
    parent_id = fields.Many2one('directory.tag', string='Parent Tag', index=True,
                                ondelete='cascade')
    child_ids = fields.One2many('directory.tag', 'parent_id', string='Child Tags')
    active = fields.Boolean(default=True,
                            help="The active field allows you to hide the directory tag without removing it.")
    parent_path = fields.Char(index=True)
    parent_left = fields.Integer(string='Left parent', index=True)
    parent_right = fields.Integer(string='Right parent', index=True)

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('Error ! You can not create recursive tags.'))

    def name_get(self):
        """ Return the directory tags' display name, including their direct
            parent by default.
        """
        res = []
        for tag in self:
            names = []
            current = tag
            while current:
                names.append(current.name)
                current = current.parent_id
            res.append((tag.id, ' / '.join(reversed(names))))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args
        return self.search(args, limit=limit).name_get()


class DocumentTag(models.Model):
    _description = 'Document Tags'
    _name = 'document.tag'
    _order = 'parent_left, name'
    _parent_store = True
    _parent_order = 'name'

    name = fields.Char(string='Tag Name', required=True, translate=True)
    parent_id = fields.Many2one('document.tag', string='Parent Tag', index=True,
                                ondelete='cascade')
    child_ids = fields.One2many('document.tag', 'parent_id', string='Child Tags')
    active = fields.Boolean(default=True,
                            help="The active field allows you to hide the document tag without removing it.")
    parent_path = fields.Char(index=True)
    parent_left = fields.Integer(string='Left parent', index=True)
    parent_right = fields.Integer(string='Right parent', index=True)

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('Error ! You can not create recursive tags.'))

    def name_get(self):
        """ Return the document tags' display name, including their direct
            parent by default.
        """
        res = []
        for tag in self:
            names = []
            current = tag
            while current:
                names.append(current.name)
                current = current.parent_id
            res.append((tag.id, ' / '.join(reversed(names))))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args
        return self.search(args, limit=limit).name_get()
