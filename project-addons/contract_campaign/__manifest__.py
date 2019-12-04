# -*- encoding: utf-8 -*-
{
    'name' : 'HS - Campaign in projects',
    'version' : '12.0.0.0.0',
    'category' : 'Custom',
    'author'  : 'CMNT',
    'license' : 'AGPL-3',
    'depends' : ['project', 'sale_crm', 'sale_timesheet'],
    'data' : ['views/project_view.xml',
              'views/res_partner_view.xml',
              'views/account_invoice_view.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'description': '''
This module adds new field campign in contratcs (projects).
============================================================
    '''
}
