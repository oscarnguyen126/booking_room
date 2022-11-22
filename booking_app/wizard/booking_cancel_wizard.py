from odoo import models, fields, _


class BookingCancelWizard(models.TransientModel):
    _name = 'booking.cancel.wizard'

    reason = fields.Text(string=_('Input Reason'), required=True)

    def confirm_cancel(self):
        for record in self:
            books = self.env['room.booking'].browse(self._context.get('active_ids', []))
            if books:
                books.state = 'cancelled'
                books.reason = record.reason
                books.send_mail(type='cancel')
