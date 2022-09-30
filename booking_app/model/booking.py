from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import pytz


class Booking(models.Model):
    _name = 'room.booking'
    _inherit = ['mail.thread']
    _description = 'Room booking'
    _order = 'start_time asc'
    _rec_name = 'description'

    room_id = fields.Many2one('room.room', string='Meeting room', required=True, tracking=True)
    start_time = fields.Datetime(string='Date from', required=True, tracking=True)
    stop_time = fields.Datetime(string='Date to', compute='_compute_meeting_time', required=True, tracking=True)
    description = fields.Char(string='Contents of the meeting', required=True, tracking=True)
    status = fields.Selection([('booking', 'Booking'), ('confirmed', 'Confirmed'), ], default='booking')
    requester = fields.Many2many('res.users', 'room_booking_res_user_rel', 'booking_id', 'user_id', string='Requester',
                                 index=True, default=lambda self: self.env.user, required=True)
    department = fields.Many2one('res.groups', default=lambda self: self.env.user.groups_id[0], required=True)
    partner_ids = fields.Many2many('res.partner', 'room_booking_res_partner_rel', 'booking_id', 'partner_id',
                                   string='Participants', required=True)
    
    @api.constrains('start_time')
    def check_room(self):
        bookings = self.env['room.booking'].search([('room_id', '=', self.room_id.id), ('id', '!=', self.ids)])
        for book in bookings:
            if book.start_time <= self.start_time < book.stop_time or book.start_time < self.stop_time < book.stop_time:
                raise ValidationError('This room has been booked by another user')

    def cancel_button(self):
        super(Booking, self).unlink()
        return {
            'type': 'ir.actions.act_url',
            'url': 'http://localhost:8015/web#cids=1&menu_id=96&action=123&model=room.booking&view_type=calendar',
            'target': 'self'
        }
        
    def confirm_button(self):
        self.ensure_one()
        tz = pytz.timezone(self.env.user.tz or 'UTC')
        start_time = self.start_time + self.start_time.astimezone(tz).utcoffset()
        stop_time = self.stop_time + self.stop_time.astimezone(tz).utcoffset()
        values = {
            'start_time': start_time,
            'stop_time': stop_time,
            'object': self,
            'tz': tz.zone
        }
        view = self.env['ir.ui.view'].browse(
            self.env['ir.model.data']._xmlid_to_res_id('booking_app.template_email_send_booking'))
        assignation_msg = view._render(values, engine='ir.qweb', minimal_qcontext=True)
        assignation_msg = self.env['mail.render.mixin']._replace_local_links(assignation_msg)
        ctx = {
            'default_model': 'room.booking',
            'default_res_id': self.ids[0],
            'default_use_template': False,
            'default_body': assignation_msg,
            'default_partner_ids': self.partner_ids.ids,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': 'mail.mail_notification_light',
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
        }
        mail_compose = self.env['mail.compose.message'].with_context(ctx).create({'subject': _('Confirmation Email')})
        mail_compose.action_send_mail()
        self.status = 'confirmed'

    @api.constrains('start_time')
    def block_booking_in_past(self):
        if self.start_time < datetime.now():
            raise ValidationError("The time of the meeting must be equal or greater than now!")

    @api.depends('start_time')
    def _compute_meeting_time(self):
        for record in self:
            record.stop_time = record.start_time + timedelta(hours=2)
