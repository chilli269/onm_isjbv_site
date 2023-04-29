from odoo import http
d="5"
class controller(http.Controller):
    @http.route('/testing2/controller'+d, auth='public')
    def index(self):
        
        houses=http.request.env['testing2_module'].search([])
        x="<h1>Uite:"
        for house in houses:
            x+=" si "
            x+=house.name
        x+="</h1>"
        return x

    @http.route('/testing2/<model("testing2_module"):hn>/house-info', auth='public', website=True)
    def display_test1(self,hn):
        return http.request.render('testing2.second_template', {
            'hn': hn
        })
    
    @http.route('/testing2/<model("testing2_module"):hn>/owner-info', auth='public', website=True)
    def display_test2(self,hn):
        return http.request.render('testing2.third_template', {
            'hn': hn
        })