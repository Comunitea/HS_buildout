from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, AccessError, MissingError, UserError
from odoo.http import content_disposition, Controller, request, route
import json

GOOGLEADS_TO_LEAD = {
    "FULL_NAME":"contact_name",
    "EMAIL":"email_from",
    "PHONE_NUMBER":"phone",
    "POSTAL_CODE":"zip",
    "STREET_ADDRESS":"street",
    "CITY":"city",
    "COUNTRY":"country_id"}

class GoogleAdsController(Controller):

    @route('/google_ads_webhook/get_data', type='json', auth='public', csrf=False, methods=['POST'],cors='*')
    def get_data(self, **kwargs):
        try:
            lead = request.env['crm.lead'].sudo()
            data = json.loads(request.httprequest.data.decode('utf-8'))
            if not data.get('google_key',False):
                return {'result': 'error', 'error': 'Google key not found'}
            company = request.env['res.company'].sudo().search([('google_ads_key','=',data.get('google_key'))],limit=1)
            if not company:
                return {'result': 'error', 'error': 'Incorrect Google key'}
            vals = {}
            google_key = data.get('google_key')
            values = data.get('user_column_data')
            for data in values:
                if data.get('column_id',False) in GOOGLEADS_TO_LEAD:
                    vals[GOOGLEADS_TO_LEAD[data.get('column_id')]] = data.get('string_value')
            vals['name'] = vals['contact_name'] if vals.get('contact_name',False) else 'Cupón desde Google Ads'
            campaign = request.env.ref('google_ads_integration.google_ads_lead')
            vals['campaign_id'] = campaign.id
            lead_id = lead.create(vals)
            return {'result': 'success', 'data': str(lead_id.id)}
        except Exception as e:
            return {'result': 'error', 'error': str(e)}
