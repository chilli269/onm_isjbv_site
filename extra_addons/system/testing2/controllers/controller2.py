from odoo import http

class controller(http.Controller):
    @http.route('/testing2/controller', auth='user', website=True)
    def index(self, **kw):
        
        house_list=http.request.env['testing2_module'].search([])

        return http.request.render('testing2.first_template', {
            'houses': house_list
        })