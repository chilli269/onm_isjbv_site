
from odoo import models,fields,api,_
import logging
_logger=logging.getLogger(__name__)
  


class Notepad(models.Model):
   _name='my.notepad'
   name=fields.Char(string='Note')
   state=fields.Selection([('todo','To Do'),('done','Done'),('in_progress','In Progress')],string='State') 
