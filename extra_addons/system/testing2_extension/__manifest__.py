{
    'name': 'Testing2 Extension',
    'version': '1',
    'category': 'project',
    'summary': 'Testing2 Module Extension',
    'description': """
    """,
    'author': 'Mihnea',
    'depends': [
        'base','website'
        ],
    'data': [
        'views/extending.xml'
        ],
    'assets': {
        'web.assets_frontend': [
            'testing2_extension/static/src/css/style.css',
        ],
    },
    'installable': True,
    'auto_install': False,
}