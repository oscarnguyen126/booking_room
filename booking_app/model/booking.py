from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
import pytz


class Booking(models.Model):
    _name = 'room.booking'
    _inherit = ['mail.thread']
    _description = 'Room booking'
    _order = 'start_time asc'
    _rec_name = 'title'

    room_id = fields.Many2one('room.room', string=_("Meeting room"), required=True, tracking=True)
    start_time = fields.Datetime(string=_("Start date"), required=True, tracking=True, copy=False)
    stop_time = fields.Datetime(string=_("Stop date"), required=True, tracking=True, copy=False)
    title = fields.Char(string=_("Title"), required=True, tracking=True)
    description = fields.Text(string=_("Content"), tracking=True)
    state = fields.Selection([('booking', 'Booking'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')],
                              default='booking', string=_("State"))
    requester = fields.Many2one('res.users', index=True, string=_("Requester"),
                                default=lambda self: self.env.user)
    department_id = fields.Many2one('hr.department', string=_("Department"), compute='compute_requester')
    partner_ids = fields.Many2many('res.partner', 'room_booking_res_partner_rel', 'booking_id', 'partner_id',
                                   string=_("Participants"))
    during = fields.Float(string=_('Using time'), store=True, compute='_compute_during_time')
    max_volume = fields.Integer(related='room_id.volume', string=_('Max volume'))
    reason = fields.Char(string=_('Input Reason'), readonly=True)
    attached_file = fields.Binary(string=_('Attached File'))
    note = fields.Text(string=_('Requirements'))
    edit_checker = fields.Boolean(default=True)

    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            if rec.edit_checker is True and rec.state == 'confirmed' and not vals.get('edit_checker', False):
                rec.send_mail(type='edited')
                rec.write({
                    'edit_checker': False
                    })
        return res

    @api.constrains('start_time', 'stop_time')
    def check_duplicate(self):
        for record in self:
            bookings = self.env['room.booking'].search(["&", ('room_id', '=', record.room_id.id), ('id', '!=', record.ids)])
            for book in bookings:
                if book.start_time <= record.start_time < book.stop_time or book.start_time < record.stop_time < book.stop_time:
                    raise ValidationError(_('The room has been booked!'))

    @api.constrains('start_time')
    def block_booking_in_past(self):
        if self.start_time < datetime.now():
            raise ValidationError(_("The start time must be greater than now"))

    @api.constrains('start_time', 'stop_time')
    def check_stop_time(self):
        if self.stop_time <= self.start_time:
            raise ValidationError(_("The stop time must be greater than the start time"))

    @api.depends('start_time', 'stop_time', 'state')
    def _compute_during_time(self):
        for record in self:
            if record.state == 'confirmed':
                tz = self.env.user.tz if self.env.user.tz else 'UTC'
                record.during = 0
                if record.start_time and record.stop_time:
                    start_time = record.start_time.astimezone(pytz.timezone(tz))
                    stop_time = record.stop_time.astimezone(pytz.timezone(tz))
                    during = stop_time - start_time
                    if during.days:
                        record.during = during.seconds + during.days * 86400 / 3600
                    else:
                        record.during = during.seconds / 3600
            else:
                record.during = 0

    @api.depends('requester')
    def compute_requester(self):
        for rec in self:
            rec.department_id = False
            if rec.requester:
                rec.department_id = rec.requester.employee_id.department_id

    def send_mail(self, type=''):
        self.ensure_one()
        tz = pytz.timezone(self.env.user.tz or 'UTC')
        start_time = self.start_time
        stop_time = self.stop_time
        values = {
            'start_time': start_time,
            'stop_time': stop_time,
            'object': self,
            'tz': tz.zone
        }
        if type == 'cancel':
            view = self.env['ir.ui.view'].browse(
                self.env['ir.model.data']._xmlid_to_res_id('booking_app.cancel_email_template'))
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
            mail_compose = self.env['mail.compose.message'].with_context(ctx).create(
                {'subject': '[TB] HỦY LỊCH HỌP - ' + self.title})
            mail_compose.action_send_mail()
        elif type == 'confirmed':
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
            mail_compose = self.env['mail.compose.message'].with_context(ctx).create(
                {'subject': '[TB] LỊCH HỌP - ' + self.title})
            mail_compose.action_send_mail()
        else:
            view = self.env['ir.ui.view'].browse(
                self.env['ir.model.data']._xmlid_to_res_id('booking_app.edit_email_template'))
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
            mail_compose = self.env['mail.compose.message'].with_context(ctx).create(
                {'subject': '[TB] THAY ĐỔI LỊCH HỌP - ' + self.title})
            mail_compose.action_send_mail()

    def cancel_button(self):
        action = self.env.ref('booking_app.action_input_reason_wizard').read()[0]
        self.edit_checker = False
        return action

    def confirm_button(self):
        for record in self:
            record.state = 'confirmed'
            record.send_mail(type='confirmed')
            record.edit_checker = False

    def edit_button(self):
        for record in self:
            record.edit_checker = True

    def back_to_draft(self):
        for record in self:
            record.state = 'booking'

    @api.onchange('start_time')
    def oneday(self):
        for record in self:
            if record.start_time:
                record.stop_time = record.start_time.replace(day=record.start_time.day, month=record.start_time.month,
                                                             year=record.start_time.year)

    @api.constrains('partner_ids')
    def check_quantity_guess(self):
        for record in self:
            if len(record.partner_ids) > record.room_id.volume:
                raise ValidationError(_('The guesses is greater than volume of the room'))

    @api.constrains('start_time', 'stop_time')
    def limit_time(self):
        for record in self:
            if record.stop_time.strftime('%m/%d/%Y') > record.start_time.strftime('%m/%d/%Y'):
                raise ValidationError('Using time is too long')

