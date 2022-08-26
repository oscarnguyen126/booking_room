from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class Booking(models.Model):
    _name = 'room.booking'
    _inherit= ['mail.thread']
    _description = 'Room booking'
    _order = 'start_time asc'
    _rec_name = 'description'

    room_id = fields.Many2one('room.room', string='Meeting room', required=True, tracking=True)
    start_time = fields.Datetime(string='Date from', required=True, tracking=True)
    stop_time = fields.Datetime(string='Date to', required=True, tracking=True)
    description = fields.Char(string='Contents of the meeting', required=True, tracking=True)
    status = fields.Selection([('booking','Booking'),('confirmed','Confirmed'),], default='booking')
    requester = fields.Many2many('res.users', 'room_booking_res_user_rel', 'booking_id', 'user_id', string='Requester', index=True, default=lambda self: self.env.user, required=True)
    department = fields.Many2one('res.groups')
    partner_ids = fields.Many2many('res.partner', 'room_booking_res_partner_rel', 'booking_id', 'partner_id', string='Participants')


    @api.constrains('start_time')
    def check_room(self):
        bookings = self.env['room.booking'].search([('room_id','=',self.room_id.id), ('id','!=',self.id)])
        for book in bookings:
            if book.start_time <= self.start_time < book.stop_time or book.start_time < self.stop_time <book.stop_time:
                raise ValidationError('Room booked')


    def confirm_button(self):
        self.status = 'confirmed'
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
            'default_composition_mode': 'comment' if len(self.partner_ids) == 1 else 'mass_mail',
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


    def cancel_button(self):
        super(Booking,self).unlink()
        return {
            'type': 'ir.actions.act_url',
            'url': 'http://localhost:8069/web#cids=1&menu_id=208&action=311&model=room.booking&view_type=calendar',
            'target': 'self'
        }


    @api.model
    def message_get_reply_to(self, res_ids, default=None):
        record = self.sudo().browse(res_ids)
        reply_to = record.create_uid.email
        return {res_ids[0]: reply_to}
