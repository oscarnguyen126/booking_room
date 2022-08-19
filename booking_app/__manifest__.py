{
    'name': 'Booking room',
    'version': '1.0',
    'application': True,
    'depends': ['base', 'mail','sale'],
    'data': ['security/ir.model.access.csv',
             'views/room_views.xml',
             'views/room_booking_menu.xml',
             'views/room_booking_views.xml',
             'data/email_template.xml'],
    'license': 'GPL-3',
}
