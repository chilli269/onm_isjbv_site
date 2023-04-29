from odoo import models, fields, api, _


class Testing(models.Model):
    _name='testing_module'
    _description='This is a testing module'

    name=fields.Char(string='Your First Name', required=True)
    surname=fields.Char(string='Your Last Name', required=True)
    age=fields.Integer(default='19', readonly=True)
    state=fields.Selection([('unborn', 'Unborn'),('alive', 'Alive'),('dead', 'Dead'),('exploded', 'Exploded')], string="Select the state of the person:", required=True)
    active=True