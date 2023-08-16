# Author: Omar Castiñeira Saavedra
# Copyright 2020 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'HS Field Service',
    'version': '12.0.0.0.0',
    'category': 'Field Services',
    'author': 'Comunitea',
    "website": "https://comunitea.com",
    'depends': [
        'hr_timesheet',
        'project_task_digitized_signature',
        'sale_order_type',
        'project_task_material_stock',
        'project_status',
        'hs_custom',
        'project_stage_closed',
        'project_task_send_by_mail'
    ],
    'data': ['security/hs_field_service_security.xml',
             'security/ir.model.access.csv',
             'wizard/wzd_attach_pictures_view.xml',
             'wizard/wzd_project_attach_pictures_view.xml',
             'views/project_task_view.xml',
             'views/project_project_view.xml',
             'views/field_service_menuitems.xml',
             'data/hs_field_service_data.xml',
             'views/project_task_report.xml',],
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
