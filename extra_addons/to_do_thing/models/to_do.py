# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ToDo(models.Model):
    _name = 'my.todo'

    name = fields.Char(string='Name')
    state = fields.Selection([('todo', 'ToDo'),
                              ('progress', 'In progress'),
                              ('done', 'Done')],
                             default='todo',
                             string='State')

    def action_progress(self):
        if self.name:
            self.state = 'progress'
        else:
            _logger.info('\n\n\n\n NAME IS REQUIRED !!!!! \n\n\n')

    def action_done(self):
        partners = self.env['res.partner'].search([]).ids
        _logger.info('\n\n\n\n partners = %s \n\n\n', partners)
        _logger.info('\n\n\n\n type = %s \n\n\n', type(partners))
        product_category = self.env['product.category'].search([])
        products = self.env['product.template'].search([('purchase_ok', '=', True)])
        _logger.info('\n\n\n\n products = %s \n\n\n', products)
        ids_list = [3, 10]
        _logger.info('\n\n\n\n ids_list = %s \n\n\n', ids_list)
        cond = self.prepare_in_dict_condition(ids_list)
        _logger.info('\n\n\n\n cond = %s \n\n\n', cond)

        products = self.sudo().get_records_from_model('product.template',
                                                      f"id {cond}")
        _logger.info('\n\n\n\n products2 = %s \n\n\n', products)
        self.state = 'done'

    def prepare_in_dict_condition(self, value):
        if len(value) > 1:
            cond = f"IN {tuple(value)}"
        elif len(value) == 1:
            cond = f"= {value[0]}"
        else:
            cond = f"= 0"
        return cond


    def get_records_from_model(self, model, condition):
        """
        :param model: Example str() = 'sale.order'
        :param condition:  Example str() = f"partner_id = '{partner.id}' AND NOT state = 'draft'"
        :return: recordset or False
        """
        records = False
        if model and condition:
            model_for_request = str(model).replace(".", "_")
            self.env.cr.execute(f'SELECT id FROM {model_for_request} WHERE {condition}')
            records = [i['id'] for i in self.env.cr.dictfetchall()]
            if records:
                records = self.env[f'{model}'].sudo().browse(records)
        _logger.info('\n\n result = %s \n\n', records)
        return records
