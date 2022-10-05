{
    'name': 'Booking room',
    'version': '1.0',
    'application': True,
    'installable': True,
    'depends': ['base', 'mail'],
    'data': ['security/ir.model.access.csv',
             'views/room_views.xml',
             'views/room_booking_views.xml',
             'views/room_booking_menu.xml',
             'data/email_template.xml',
             'data/cancel_email_template.xml'],
    'license': 'GPL-3',
}
