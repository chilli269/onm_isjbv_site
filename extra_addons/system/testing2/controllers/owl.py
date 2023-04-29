from odoo import http

class controller(http.Controller):
    @http.route('/mamisor', auth='user', website=True)
    def index(self, **kw):
        x = """<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8" />
                <title>IRINGO</title>
                <link rel="stylesheet" href="/testing2/static/src/css/template.css">
                <script src="/testing2/static/src/js/owl.js"></script>   
            </head>
            <body>
                <script src="/testing2/static/src/js/iringo.js"></script>
                <p>mamam</p>
            </body>
            </html>"""
        return x