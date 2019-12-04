# -*- coding: utf-8 -*-
from odoo import api, models


class CrmLead(models.Model):

    _inherit = "crm.lead"

    def _onchange_partner_id_values(self, partner_id):
        vals = super()._onchange_partner_id_values(partner_id)
        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)
            if partner.campaign_id:
                vals.update({'campaign_id': partner.campaign_id.id,
                             'source_id': partner.source_id.id,
                             'medium_id': partner.medium_id.id})
        return vals

    @api.multi
    def _convert_opportunity_data(self, customer, team_id=False):
        vals = super()._convert_opportunity_data(customer, team_id=team_id)
        if customer:
            vals.update({'campaign_id': customer.campaign_id.id,
                         'source_id': customer.source_id.id,
                         'medium_id': customer.medium_id.id})
        return vals

    @api.multi
    def _create_lead_partner_data(self, name, is_company, parent_id=False):
        vals = super()._create_lead_partner_data(name, is_company,
                                                 parent_id=parent_id)
        vals.update({'campaign_id': self.campaign_id.id,
                     'source_id': self.source_id.id,
                     'medium_id': self.medium_id.id})
        return vals
