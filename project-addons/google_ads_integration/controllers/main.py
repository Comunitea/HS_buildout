from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, AccessError, MissingError, UserError
from odoo.http import content_disposition, Controller, request, route, Response
import json
from odoo.addons.web.controllers.main import CSVExport
from datetime import datetime
from dateutil.relativedelta import relativedelta

GOOGLEADS_TO_LEAD = {
    "FULL_NAME":"contact_name",
    "EMAIL":"email_from",
    "PHONE_NUMBER":"phone",
    "POSTAL_CODE":"zip",
    "STREET_ADDRESS":"street",
    "CITY":"city",
    "COUNTRY":"country_id"}

CONVERSION_NAME = {
    "invalid": _("Invalid Lead"),
    "valid": _("Valid Lead"),
    "qualified": _("Qualified Lead"),
    "sale": _("Sale")
}

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
            vals['user_id'] = False
            if vals.get('zip',False):
                zip_id = request.env['res.city.zip'].sudo().search([('name','=',vals.get('zip'))],limit=1)
                if zip_id:
                    vals['state_id'] = zip_id.city_id.state_id.id
            lead.create(vals)
            return  {'result': 'success'}
        except Exception as e:
            return {'result': 'error', 'error': str(e)}

class CSVExportGoogle(CSVExport):

    @route('/get_google_data/<string:token>', type='http', auth='public', csrf=False, methods=['GET'],cors='*')
    def get_google_data(self,token, **kwargs):
        if not token:
            return Response('Token not found', status=404)
        company = request.env['res.company'].sudo().search([('google_ads_key','=',token)],limit=1)
        if not company:
            return Response('Incorrect token', status=404)
        CRM = request.env['crm.lead'].sudo()
        date = fields.Datetime.now() - relativedelta(days=90)
        leads = CRM.search([('gclid','!=',False),('creation_date','>=',date)])
        if leads:
            column_headers = ["Google Click ID","Conversion Name","Conversion Time","Conversion Value","Conversion Currency"]
            rows = []
            for lead in leads:
                rows.append([lead.gclid,
                             (CONVERSION_NAME[lead.stage_id.conversion_name] if lead.stage_id.conversion_name else 'Valid Lead')+" "+lead.gclid,
                             lead.creation_date.strftime('%Y-%m-%d %H:%M:%S'),
                             lead.expected_revenue,
                             lead.company_currency.name])
            data = self.from_data(column_headers, rows)
            return request.make_response(
                data,
                headers=[
                    ('Content-Disposition', content_disposition('google_ads_data.csv')),
                    ('Content-Type', 'text/csv')
                ]
            )
        return Response('No data found', status=404)
