# -*- coding: utf-8 -*-
{
    'name': "PWA App",

    'summary': """
    """,

    'description': """
       
    """,

    'author': "Odoo Evangelist",
    'website': "http://delicloud.ro",

    'images': [],

    'category': 'App/pwa',
    'version': '15.0.0.2',

    'depends': ['base', 'web'],

    'data': [
        'security/ir.model.access.csv',
        'views/delicloud_web.xml',
        'views/delicloud_pwa_manifest.xml',
        'views/delicloud_pwa_setting.xml',
        'views/delicloud_pwa_service_worker.xml'
    ],

    'assets': {
        'web.assets_backend': [
            'delicloud_pwa/static/src/user_menu_patch.js',
        ],
        'web.assets_qweb': [],
        'web.assets_backend_prod_only': []
    }
}
