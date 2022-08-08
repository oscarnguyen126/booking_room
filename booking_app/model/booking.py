from odoo import models, fields, api
from odoo.exceptions import UserError

class Booking(models.Model):
    _name = 'room.booking'
    _description = 'Room booking'

    room_id = fields.Many2one('room.room', string='Meeting room')
    start_time = fields.Datetime()
    end_time = fields.Datetime()
    description = fields.Char(string='Content of meeting')
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')])
    staff_id = fields.Many2one('company.staff', string='Booking person')
    
    
    @api.constrains('')
    def check_duplicate(self):
        booking_list = self.env['room.booking'].search([])
        start = booking_list.mapped('start_time')
        for i in start:
            if i == i+1:
                raise UserError('Already booking this time')
    