from odoo import models, fields


class Room(models.Model):
    _name = 'room.room'
    _description = 'Room'

    name = fields.Char()
    infra = fields.Char(string='Infrastructure')
    status = fields.Selection([('used', 'Used'), ('available', 'Available')])
    booking_ids = fields.One2many('room.booking', 'room_id')
