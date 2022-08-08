from odoo import models, fields


class unit(models.Model):
    _name = 'company.unit'
    _description = 'Company unit'
    
    name = fields.Char()
    