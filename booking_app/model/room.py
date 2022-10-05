from odoo import models, fields


class Room(models.Model):
    _name = 'room.room'
    _description = 'Room'

    name = fields.Char(required=True)
    infra = fields.Char(string='Trang thiết bị')
    volume = fields.Integer(string='Sức chứa tối đa')
    booking_ids = fields.One2many('room.booking', 'room_id')
