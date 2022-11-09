from odoo import models, fields, _


class Color(models.Model):
    _name = 'room.equipment.color'

    name = fields.Char(string=_('Name'), required=True)
    equipment_id = fields.One2many('room.equipments', 'color_id')
    color = fields.Char(string=_('Color'))
