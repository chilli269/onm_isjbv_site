# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _



class School(models.Model):
    _name = 'school.db'

    name = fields.Char(string='School Name')
    city= fields.Char(string='City')
    #highschool=fields.Selection(['true','Yes'],['false','No'])


