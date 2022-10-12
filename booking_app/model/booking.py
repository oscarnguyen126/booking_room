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

    room_id = fields.Many2one('room.room', string='Phòng họp', required=True, tracking=True)
    start_time = fields.Datetime(string='Thời gian bắt đầu', required=True, tracking=True)
    stop_time = fields.Datetime(string='Thời gian kết thúc', required=True, tracking=True)
    title = fields.Char(string="Tiêu đề", required=True, tracking=True)
    description = fields.Text(string='Nội dung cuộc họp', tracking=True)
    status = fields.Selection([('booking', 'Đặt lịch họp'), ('confirmed', 'Xác nhận'), ('cancelled', 'Đã hủy')],
                              string="Trạng thái", default='booking')
    requester = fields.Many2one('res.users', string='Người đặt phòng', index=True,
                                default=lambda self: self.env.user, required=True)
    department_id = fields.Many2one('hr.department', string="Đơn vị", required=True)
    partner_ids = fields.Many2many('res.partner', 'room_booking_res_partner_rel', 'booking_id', 'partner_id',
                                   string='Người tham gia')
    during = fields.Float('Thời gian sử dụng (giờ)', store=True, compute='_compute_during_time')

    def check_duplicate(self):
        bookings = self.env['room.booking'].search(["&", ('room_id', '=', self.room_id.id), ('id', '!=', self.ids),
                                                    ('status', '=', 'confirmed')])
        for book in bookings:
            if book.start_time <= self.start_time < book.stop_time or book.start_time < self.stop_time < book.stop_time:
                raise ValidationError('Phòng họp này đã được đặt bởi nhân viên khác trước đó!')

    def cancel_button(self):
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
        self.status = 'cancelled'

    def confirm_button(self):
        self.check_duplicate()
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
        self.status = 'confirmed'

    @api.onchange('write_date')
    def change_notifications(self):
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
            {'subject': '[TB] THAY ĐỔI LỊCH HỌP - ' + self.title})
        mail_compose.action_send_mail()
        self.status = 'confirmed'

    @api.constrains('start_time')
    def block_booking_in_past(self):
        if self.start_time < datetime.now():
            raise ValidationError("Thời gian bắt đầu phải lớn hơn hoặc bằng thời gian hiện tại!")

    @api.constrains('start_time', 'stop_time')
    def check_stop_time(self):
        if self.stop_time <= self.start_time:
            raise ValidationError("Thời gian kết thúc phải lớn hơn thời gian bắt đầu")

    @api.depends('start_time', 'stop_time')
    def _compute_during_time(self):
        for record in self:
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

    @api.onchange('requester')
    def onchange_requester(self):
        for rec in self:
            if rec.requester:
                rec.department_id = rec.requester.employee_id.department_id
