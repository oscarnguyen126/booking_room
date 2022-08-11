from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Client(models.Model):
    _name = 'company.staff'
    _description = 'Company staff'
    
    name = fields.Char(string='Name')
    bday = fields.Date(string='Birthday')
    position = fields.Char(string='Position')
    email = fields.Char(string='Email address')
    team_id = fields.Many2one('company.unit')
    
    
    @api.constrains('email')
    def validate_email(self):
        for rec in self:
            if not '@' in rec.email:
                raise ValidationError('Invalid email')
