# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2022 Odoo IT now <http://www.odooitnow.com/>
# See LICENSE file for full copyright and licensing details.
#
##############################################################################
{
    'name': 'Portal Document Management: Backend + Portal',
    'category': 'Document Management',
    'summary': 'Document Management: Backend + Portal',

    'version': '15.0.1',
    'description': """
This module allow your customers to upload/download documents from My Account.
An organization can also share documents with customers/suppliers allow to view and download.
        """,

    'author': 'Odoo IT now',
    'website': 'http://www.odooitnow.com/',
    'license': 'Other proprietary',

    'depends': [
        'base',
        'portal',
        'website'
        ],
    'data': [
        'security/document_security.xml',
        'security/ir.model.access.csv',
        'data/portal_documents_data.xml',
        'views/menu_view.xml',
        'views/tags_view.xml',
        'views/res_view.xml',
        'views/directory_view.xml',
        'views/website_portal_sale_template.xml',
        'views/templates.xml',
    ],
    'images': ['images/OdooITnow_screenshot.png'],

    'price': 75,
    'currency': 'EUR',

    'installable': True,
    'application': True,
    'auto_install': False
}
