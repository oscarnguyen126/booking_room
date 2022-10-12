from odoo import models, fields


class Room(models.Model):
    _name = 'room.room'
    _description = 'Room'

    name = fields.Char(required=True)
    volume = fields.Integer(string="Sức chứa tối đa (Người)")
    equipment = fields.Many2many('room.equipments', 'room_equipments_room_room_rel', 'room_id', 'equipment_id',
                                 'Thiết bị', required=True)
    booking_ids = fields.One2many('room.booking', 'room_id')
