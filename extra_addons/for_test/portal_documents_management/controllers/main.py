# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2022 Odoo IT now <http://www.odooitnow.com/>
#
##############################################################################-

import json
import base64
from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.exceptions import ValidationError


class CustomerPortal(CustomerPortal):
 
    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        Attachment = request.env['ir.attachment'].sudo()
        # Documents count
        documents_count = Attachment.search_count([
            ('document_type', 'in', ['portal', 'normal']), '|',
            ('res_id', '=', partner.id),
            ('user_ids', 'in', request.env.user.ids)
        ])
        documents_count += Attachment.search_count([
            ('document_type', '=', 'portal'),
            ('user_ids', '=', False)
        ])
 
        values.update({
            'documents_count': documents_count,
        })
        return values

    # ------------------------------------------------------------
    # My Documents
    # ------------------------------------------------------------

    @http.route([
        '/my/documents',
        '/my/documents/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_documents(self, page=0, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        Attachment = request.env['ir.attachment'].sudo()

        domain = [
            ('document_type', 'in', ['portal', 'normal']), '|',
            ('res_id', '=', partner.id), '|',
            ('user_ids', 'in', request.env.user.ids),
            ('user_ids', '=', False)
        ]
        # archive_groups = self._get_archive_groups('ir.attachment', domain)

        # count for pager
        documents_count = Attachment.search_count(domain)
        # pager
        pager = request.website.pager(
            url="/my/documents",
            total=documents_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        # Personal Documents
        personal_documents = Attachment.search([
            ('document_type', '=', 'normal'),
            ('res_id', '=', partner.id)
            ], limit=self._items_per_page, offset=pager['offset'])

        # Public Documents
        public_documents = Attachment.search([
            ('document_type', '=', 'portal'), '|',
            ('user_ids', 'in', request.env.user.ids),
            ('user_ids', '=', False)
            ], limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'date': date_begin,
            'documents': personal_documents,
            'public_documents': public_documents,
            'page_name': 'document',
            'pager': pager,
            # 'archive_groups': archive_groups,
            'default_url': '/my/documents',
            'base_url': http.request.env["ir.config_parameter"].sudo().get_param("web.base.url"),
        })
        return request.render("portal_documents_management.website_portal_my_documents", values)

    @http.route(['/upload/docs'], type='http', auth="public",
                methods=['POST'], website=True)
    def upload_docs(self, **post):
        """ Upload own documents
        """
        user_sudo = request.env['res.users'].sudo().browse(request.uid)
        try:
            # Personal Doc
            personal_dir = request.env.ref('portal_documents_management.personal_directory')
            file = post.get('upload_docs', '')
            attach = file.stream
            f = attach.read()
            attach_vals = {
                'name': file.filename,
                'document_type': 'normal',
                'directory_id': personal_dir and personal_dir.id or False,
                'res_name': file.filename,
                'res_model': 'res.partner',
                'res_id': user_sudo and user_sudo.partner_id.id or False,
                'datas': base64.encodebytes(f),
                'partner_id': user_sudo and user_sudo.partner_id.id or False
            }
            request.env['ir.attachment'].sudo().create(attach_vals)
        except ValidationError as e:
            return json.dumps({'error_fields' : e.args[0]})
        except Exception as e:
            return json.dumps({'Error' : _('Sorry... Uploaded file is not valid OR big size! Reason: %s') % (e,)})

        return request.redirect(request.httprequest.referrer)
