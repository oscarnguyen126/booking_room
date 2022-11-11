from odoo import models, fields, _


class Room(models.Model):
    _name = 'room.room'
    _description = 'Room'

    name = fields.Char(string=_('Meeting room'), required=True)
    volume = fields.Integer(string=_("Max volume"))
    equipment = fields.Many2many('room.equipments', 'room_equipments_room_room_rel', 'room_id', 'equipment_id',
                                 string=_("Equipment"), required=True)
    booking_ids = fields.One2many('room.booking', 'room_id')
