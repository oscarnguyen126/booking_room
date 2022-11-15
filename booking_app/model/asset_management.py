from odoo import models, fields, _


class AssetManagement(models.Model):
    _name = 'asset.management'

    room_id = fields.Many2one('room.room')
    equipment_id = fields.Many2one('room.equipments')
    quantity = fields.Integer(string=_('Quantity'))
