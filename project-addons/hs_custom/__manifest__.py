# Author: Omar Castiñeira Saavedra
# Copyright 2019 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'HS customizations',
    'version': '12.0.0.0.0',
    'category': 'Custom',
    'author': 'Comunitea',
    "website": "https://comunitea.com",
    'depends': [
        'hr_timesheet',
        'crm',
        'sale',
        'partner_fax',
        'account',
        'purchase',
        'project_task_digitized_signature',
        'sale_order_type',
        'project_task_material_stock'
    ],
    'data': ['views/project_view.xml',
             'views/account_invoice_view.xml',
             'views/crm_lead_view.xml',
             'views/sale_view.xml',
             'views/sale_order_report_view.xml',
             'views/purchase_order_report_view.xml',
             'views/account_invoice_report_view.xml',
             'views/res_partner_view.xml',
             'views/project_task_report.xml'],
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
