{
    'name': 'Testing2',
    'version': '1',
    'category': 'project',
    'summary': 'Testing2 Module',
    'description': """
    """,
    'author': 'Mihnea',
    'depends': [
        'base','website'
        ],
    'data': [
        'security/ir.model.access.csv',
        'views/testing2.xml',
        'templates/template.xml',
        ],
    'assets': {
        'web.assets_frontend': [
            'testing2/static/src/css/template.css',
            'testing2/static/src/js/iringo.js'
        ],
        'web.assets_qweb': [
            'testing2/static/src/xml/*.xml'
        ],
    },
    'installable': True,
    'auto_install': False,
}