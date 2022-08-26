from odoo import models, fields, api
from datetime import datetime


class Room(models.Model):
    _name = 'room.room'
    _description = 'Room'

    name = fields.Char()
    infra = fields.Char(string='Infrastructure')
    location = fields.Char(string='Location')
    booking_ids = fields.One2many('room.booking', 'room_id')
    state = fields.Selection([('available','Available'),('using','Using')], default='available')
