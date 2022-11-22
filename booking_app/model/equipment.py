from odoo import models, fields, _


class Equipment(models.Model):
    _name = 'room.equipments'
    _description = 'Equipments'

    name = fields.Char(string=_("Name"), required=True)
    description = fields.Text(string=_('Specification'))
    color = fields.Char(string=_('Color'))
