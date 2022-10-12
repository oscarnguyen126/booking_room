from odoo import models, fields


class Equipment(models.Model):
    _name = 'room.equipments'
    _description = 'Equipments'

    name = fields.Char(string="Tên thiết bị", required=True)
    model = fields.Char(string="Nhãn hiệu")
    color = fields.Char('Màu', required=True)
