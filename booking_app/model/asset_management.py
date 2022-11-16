from odoo import models, fields, _, api


class AssetManagement(models.Model):
    _name = 'asset.management'

    room_id = fields.Many2one('room.room')
    equipment_id = fields.Many2one('room.equipments')
    brand = fields.Char(string=_('Brand'), compute='compute_brand', store=True)
    quantity = fields.Integer(string=_('Quantity'))

    @api.depends('equipment_id')
    def compute_brand(self):
        for record in self:
            if record.equipment_id:
                record.brand = record.equipment_id.brand_id.name
