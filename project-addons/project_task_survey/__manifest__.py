# Author: Vicente Ángel Gutiérrez Fernández
# Copyright 2022 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Porject tasks survey',
    'version': '12.0.0.0.0',
    'category': 'Custom',
    'author': 'Comunitea',
    "website": "https://comunitea.com",
    'depends': [
        'project',
        'survey',
        'hs_custom',
        'hs_field_service'
    ],
    'data': [
        "data/data.xml",
        "views/project_task_views.xml",
        "views/survey_user_input.xml",
    ],
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
