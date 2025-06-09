# -- coding: utf-8 --
{
    'name': 'Maintenance Ticket',
    'version': '1.0',
    'summary': 'Manage facility maintenance tickets',
    'author': 'Your Name',
    'category': 'Operations',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/maintenance_ticket_sequence.xml',
        'views/maintenance_ticket_views.xml',
    ],
    'installable': True,
    'application': True,
}
