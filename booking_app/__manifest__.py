{
    'name': 'Booking room',
    'summary': """""",
    'description': '''''',
    'author': '',
    'category': 'hr',
    'version': '1.0',
    'application': True,
    'installable': True,
    'depends': [
        'base',
        'mail',
        'hr'
    ],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/rule.xml',
        'views/room_views.xml',
        'views/room_booking_views.xml',
        'views/room_equip_views.xml',
        'views/equipment_brands.xml',
        'views/equipment_color.xml',
        'views/asset_management_view.xml',
        'wizard/booking_cancel_wizard_view.xml',
        'data/email_template.xml',
        'data/cancel_email_template.xml',
        'data/edit_booking_mail_template.xml',

        'views/room_booking_menu.xml',
    ],
    'license': 'GPL-3',
    'image': ['static/description/icon.png']
}
