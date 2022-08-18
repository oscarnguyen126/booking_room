{
    'name': 'Booking room',
    'version': '1.0',
    'application': True,
    'depends': ['base', 'mail'],
    'data': ['security/ir.model.access.csv',
             'views/room_views.xml',
             'views/room_booking_menu.xml',
             'views/room_booking_views.xml',
             'data/mail_template.xml'],
    'license': 'GPL-3',
}
