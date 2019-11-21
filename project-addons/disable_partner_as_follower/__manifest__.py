# Author: Omar Castiñeira Saavedra
# Copyright 2019 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Disable partner subscriptions by default',
    'version': '12.0.0.0.0',
    'category': 'Social',
    'author': 'Comunitea',
    "website": "https://comunitea.com",
    'depends': [
        'mail',
        'sale',
        'account',
        'project',
        'mail_recipient_uncheck'
    ],
    'data': [],
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
