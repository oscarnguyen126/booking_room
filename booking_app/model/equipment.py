from odoo import models, fields, _


class Equipment(models.Model):
    _name = 'room.equipments'
    _description = 'Equipments'

    name = fields.Char(string=_("Name"), required=True)
    brand_id = fields.Many2one('room.equipment.brands', string=_("Brand"))
    color_id = fields.Many2one('room.equipment.color', string=_("Color"), required=True)
    color_ids = fields.Char(string=_('Label'), related='color_id.color')