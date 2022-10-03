from odoo import models, fields


class Room(models.Model):
    _name = 'room.room'
    _description = 'Room'

    name = fields.Char(required=True)
    infra = fields.Char(string='Equipments')
    volume = fields.Integer(string='Max volume of the room')
    booking_ids = fields.One2many('room.booking', 'room_id')
