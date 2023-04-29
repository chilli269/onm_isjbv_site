from odoo import fields, models, api

class ExtendingTesting2(models.Model):
    _inherit = "testing2_module"

    @api.depends("size", "price")
    def _get_total_price(self):
        for record in self:
            record.total_price = str(record.size * record.price + 500 ) + "$"