from odoo import models, fields, _, api
from odoo.exceptions import ValidationError


class Room(models.Model):
    _name = 'room.room'
    _description = 'Room'

    name = fields.Char(string=_('Meeting room'), required=True)
    volume = fields.Integer(string=_("Max volume"))
    equipment = fields.Many2many('room.equipments', 'room_equipments_room_room_rel', 'room_id', 'equipment_id',
                                 string=_("Equipment"))
    booking_ids = fields.One2many('room.booking', 'room_id')
    equipment_line_ids = fields.One2many('asset.management', 'room_id', string=_('Equipments'))

    @api.constrains('name')
    def check_duplicate(self):
        for record in self:
            room = self.env['room.room'].search(["&", ('name', '=', record.name), ('id', '!=', record.ids)])
            if room:
                if len(room) > 0:
                    raise ValidationError('This room is existed')
