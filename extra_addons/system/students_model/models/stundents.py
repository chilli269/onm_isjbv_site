from odoo import models, fields, api

class Student(models.Model):
    _name='students.db'

    name=fields.Char(string='Name')
    first_name=fields.Char(string='First Name')
