from odoo import models, fields, api
from odoo.exceptions import UserError
import re


class Client(models.Model):
    _name = 'company.staff'
    _description = 'Company staff'
    
    name = fields.Char(string='Name')
    bday = fields.Date(string='Birthday')
    position = fields.Char(string='Position')
    email = fields.Char(string='Email address')
    team_id = fields.Many2one('company.unit')
    