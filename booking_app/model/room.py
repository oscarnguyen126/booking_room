from odoo import models, fields, api
from datetime import datetime


class Room(models.Model):
    _name = 'room.room'
    _description = 'Room'

    name = fields.Char()
    infra = fields.Char(string='Infrastructure')
    location = fields.Char(string='Location')
    status = fields.Selection([('available', 'Available'), ('booking', 'Booking'), ('used', 'Used')], default='available')
    booking_ids = fields.One2many('room.booking', 'room_id')



    @api.constrains('booking_ids')
    def check_booking(self):
        requests = self.env['room.room'].search([('id','=',self.booking_ids.room_id.id)])
        print(requests)
        if requests:
            self.status = 'booking'
        else:
            self.status = 'available'
