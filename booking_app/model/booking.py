from urllib import request
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class Booking(models.Model):
    _name = 'room.booking'
    _description = 'Room booking'
    _order = 'start_time asc'
    _rec_name = 'room_id'

    room_id = fields.Many2one('room.room', string='Meeting room',required=True)
    start_time = fields.Datetime(string='Date from', required=True)
    stop_time = fields.Datetime(string='Date to', required=True)
    description = fields.Char(string='Content of meeting')
    booking_cycle = fields.Boolean()
    cycle_time = fields.Selection([('week','Week'),('month','Month'),('year','Year')])
    to_date = fields.Date()
    requester = fields.Many2many('res.users', index=True, default=lambda self: self.env.user, request=True)
    staff_ids = fields.Many2many('res.partner')


    @api.constrains('start_time','end_time')
    def check_room(self):
        bookings = self.env['room.booking'].search([('room_id','=',self.room_id.id),('start_time','=',self.start_time), ('id','!=',self.id)])
        if bookings:
            raise ValidationError('Room is booked')
