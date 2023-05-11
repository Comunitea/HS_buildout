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
    'notes': 'description'
}
sale_types = {
    'radoncontrol.es': 'Radon Control'
}
record.user_id = False
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
        for key in sale_types.keys():
            if key in message.email_from:
                sale_type_id = env['sale.order.type'].sudo().search(
                    [('name', '=ilike', (sale_types[key]))], limit=1)
                if sale_type_id:
                    _dict['sale_type_id'] = sale_type_id.id
                break
        if not _dict.get('sale_type_id'):
            sale_type_id = env['sale.order.type'].search([], limit=1)
            if sale_type_id:
                _dict['sale_type_id'] = sale_type_id.id
        record.write(_dict)
        record._onchange_state_id()
        record.create_opportunity()

