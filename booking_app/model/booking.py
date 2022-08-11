from time import timezone
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class Booking(models.Model):
    _name = 'room.booking'
    _description = 'Room booking'
    _order = 'start_time asc'

    room_id = fields.Many2one('room.room', string='Meeting room')
    start_time = fields.Datetime(required=True)
    end_time = fields.Datetime(required=True)
    description = fields.Char(string='Content of meeting')
    staff_ids = fields.Many2many('company.staff', string='Attendants', required=True)


    @api.constrains('start_time', 'end_time')
    def check_avalable(self):
        for rec in self:
            current = datetime.now()
            start = rec.start_time
            end = rec.end_time
            if start <= current <= end:
                rec.room_id.status = 'used'
            elif end <= current:
                rec.room_id.status = 'available'
                print(rec.room_id.status)
                print(end)
            elif not start:
                rec.room_id.status = 'available'
