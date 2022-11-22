from odoo import models, fields, _, api


class AssetManagement(models.Model):
    _name = 'asset.management'

    room_id = fields.Many2one('room.room')
    equipment_id = fields.Many2one('room.equipments')
    description = fields.Text(related='equipment_id.description', string=_('Description'))
    quantity = fields.Integer(string=_('Quantity'))
