fields = {
    'name': 'contact_name',
    'Nombre': 'contact_name',
    'phone': 'phone',
    'Teléfono': 'phone',
    'city': 'city',
    'Población': 'city',
    'zip': 'zip',
    'email': 'email_from',
    'Email': 'email_from',
    'E-mail': 'email_from',
    'notes': 'description',
    'Código Postal': 'zip'
}
sale_types = {
    'radoncontrol.es': 'Radon Control'
}
record.write({'user_id': False})
for message in record.message_ids.filtered(lambda m: m.message_type == 'email'):
    _dict = {}
    lines = message.body.split('\n')
    for i, line in enumerate(lines):
        for key, field in fields.items():
            if key in line:
                split_line = line.split(':')
                if len(split_line) > 1 and split_line[1].strip():
                    _dict[field] = split_line[1].strip()
                else:
                    _dict[field] = lines[i+1].strip()
                break
    if _dict:
        if _dict.get('zip'):
            zip_id = env['res.city.zip'].sudo().search([(
                'name', '=', _dict['zip'])], limit=1)
            if zip_id:
                _dict['state_id'] = zip_id.city_id.state_id.id
        if _dict.get('contact_name'):
            _dict['name'] = _dict['contact_name']
        for key in sale_types.keys():
            if key in message.email_from:
                sale_type_id = env['sale.order.type'].sudo().search(
                    [('name', '=ilike', (sale_types[key]))], limit=1)
                if sale_type_id:
                    _dict['sale_type_id'] = sale_type_id.id
                    _dict['campaign_id'] = 60
                break
        if not _dict.get('sale_type_id'):
            sale_type_id = env['sale.order.type'].search([], limit=1)
            if sale_type_id:
                _dict['sale_type_id'] = sale_type_id.id
                if 'humedades.hogarseco.com' in message.email_from:
                    _dict['campaign_id'] = 21
                else:
                    _dict['campaign_id'] = 19
        record.write(_dict)




# from odoo.addons.phone_validation.tools import phone_validation
# from odoo import exceptions
# crm_leads = env['crm.lead'].search(['&','&','&',('active','=',True),('probability','<',100),('phone','!=',False),('stage_id','!=',stage.id)])
# errores= []
# for lead in crm_leads:
#     try:
#         number = lead.phone_format_custom(lead.phone, company=lead.company_id)
#     except Exception as e:
#         errores.append(e)
#         number = e
#     try:
#         if not isinstance(number, Exception) and lead.phone != number:
#             lead.managed = True
#             lead.phone = number
#     except Exception as f:
