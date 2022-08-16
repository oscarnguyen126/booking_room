from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class Booking(models.Model):
    _name = 'room.booking'
    _description = 'Room booking'
    _order = 'start_time asc'
    _rec_name = 'room_id'

    room_id = fields.Many2one('room.room', string='Meeting room')
    start_time = fields.Datetime(required=True)
    stop_time = fields.Datetime(required=True)
    description = fields.Char(string='Content of meeting')
    booking_cycle = fields.Boolean()
    cycle_time = fields.Selection([('week','Week'),('month','Month'),('year','Year')])
    to_date = fields.Date(required=True)
    staff_ids = fields.Many2many('company.staff', string='Attendants', required=True)


    @api.constrains('start_time')
    def check_room(self):
        bookings = self.env['room.booking'].search([('room_id','=',self.room_id.id)])
        for booking in bookings:
            if booking.start_time < self.start_time < booking.stop_time:
                raise ValidationError('Room booked')
