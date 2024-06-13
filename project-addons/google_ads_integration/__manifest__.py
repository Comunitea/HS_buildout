{
    'name': 'Google Ads Integration',
    'version': '12.0.0.1.0',
    'description': 'Google Ads Integration',
    'author': 'comunitea',
    'website': 'www.comunitea.com',
    'license': 'LGPL-3',
    'category': 'custom',
    'depends': [
        'base',
        'crm',
        'utm'
    ],
    'data': [
        'views/res_company_views.xml',
        'data/campaign.xml'],
    'auto_install': False,
    'application': False,
    'installable': True,
}
