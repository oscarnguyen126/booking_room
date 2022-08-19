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
    requester = fields.Many2many('res.users', index=True, default=lambda self: self.env.user, required=True)
    partner_ids = fields.Many2many('res.partner')


    @api.constrains('start_time')
    def check_room(self):
        bookings = self.env['room.booking'].search([('room_id','=',self.room_id.id),('start_time','=',self.start_time), ('id','!=',self.id)])
        if bookings:
            raise ValidationError('Room is booked')

    
    def action_quotation_send(self):
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()
        template_id = self.env['ir.model.data']._xmlid_to_res_id('booking_app.mail_bookroom_confirmation', raise_if_not_found=False)
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'room.booking',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
