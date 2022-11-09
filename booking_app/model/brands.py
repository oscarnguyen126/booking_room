from odoo import models, fields, _


class Models(models.Model):
    _name = 'room.equipment.brands'

    name = fields.Char(string=_('Name'), required=True)
    equipment_id = fields.One2many('room.equipments', 'brand_id')
