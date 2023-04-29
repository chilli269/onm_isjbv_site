from odoo import models, fields, api, _


class Testing2(models.Model):
    _name='testing2_module'
    _description='This is a testing2 module'

    name=fields.Char(string="The name of the house.", required=True)
    address=fields.Char(string="The address of the house", required=True)
    size=fields.Float(string="The size of the house", required=True)
    size_output=fields.Char(compute="_get_house_size", string="The size of the house")
    price=fields.Float(required=True, default='10')
    total_price=fields.Char(compute="_get_total_price")
    state=fields.Selection([('on_market', 'On Market'), ('sold', 'Sold'), ('not_on_market', 'Not On Market')], required=True)
    owner_name_id=fields.Many2one('testing_module', string="Owner")
    owner_full_name=fields.Char(compute="_get_owner_full_name")
    link=fields.Char(string="Link", required=True)
    number_of_records=fields.Char(compute="_number_of_records")

    @api.depends("size", "price")
    def _get_total_price(self):
        for record in self:
            record.total_price = str(record.size * record.price) + "$"

    @api.depends("owner_name_id")
    def _get_owner_full_name(self):
        for record in self:
            record.owner_full_name=record.owner_name_id.name + " " + record.owner_name_id.surname

    @api.depends("size")
    def _get_house_size(self):
        for record in self:
            record.size_output=str(record.size) + " square meters"

    @api.depends("state")
    def house_sold(self):
        for record in self:
            record.state='sold'
        return True

    @api.depends("state")
    def house_on_market(self):
        for record in self:
            record.state='on_market'
        return True
    
    @api.depends("state")
    def house_not_on_market(self):
        for record in self:
            record.state='not_on_market'
        return True


    def property_info(self):
        for record in self:
            return{
                "type": "ir.actions.act_url",
                "url": record.link,
                "target": "new",
            }
    

    def owner_info(self):
        for record in self:
            return{
                "type": "ir.actions.act_window",
                "res_model": "testing_module",
                "views": [[False, "form"]],
                "res_id": record.owner_name_id.id,
                "target": "self",
                }
    
    @api.depends("number_of_records")
    def _number_of_records(self):
        for record in self:
            record.number_of_records = self.env['testing2_module'].search_count([('price', '>=', '0')])
        
    

    

