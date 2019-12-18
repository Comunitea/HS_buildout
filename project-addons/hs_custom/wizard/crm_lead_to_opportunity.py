# Author: Omar Castiñeira Saavedra
# Copyright 2019 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class Lead2OpportunityPartner(models.TransientModel):

    _inherit = 'crm.lead2opportunity.partner'

    @api.model
    def _get_duplicated_leads_by_phone(self, partner_id, phone,
                                       include_lost=False):
        if not phone:
            return self.env['crm.lead']
        partner_match_domain = [('phone', '=', phone)]
        if partner_id:
            partner_match_domain.append(('partner_id', '=', partner_id))
        partner_match_domain = ['|'] * (len(partner_match_domain) - 1) + \
            partner_match_domain
        if not partner_match_domain:
            return self.env['crm.lead']
        domain = partner_match_domain
        if not include_lost:
            domain += ['&', ('active', '=', True), ('probability', '<', 100)]
        else:
            domain += ['|', '&', ('type', '=', 'lead'), ('active', '=', True),
                       ('type', '=', 'opportunity')]
        return self.env['crm.lead'].search(domain)

    @api.model
    def default_get(self, fields):
        """ Default get for name, opportunity_ids.
            If there is an exisitng partner link to the lead, find all existing
            opportunities links with this partner to merge all information
            together
        """
        result = super(Lead2OpportunityPartner, self).default_get(fields)
        if self._context.get('active_id'):
            tomerge = {int(self._context['active_id'])}

            partner_id = result.get('partner_id')
            lead = self.env['crm.lead'].browse(self._context['active_id'])
            email = lead.partner_id.email if lead.partner_id else \
                lead.email_from
            phone = lead.partner_id.phone if lead.partner_id else lead.phone

            tomerge.update(self._get_duplicated_leads(partner_id, email,
                                                      include_lost=True).ids)
            tomerge.update(self.
                           _get_duplicated_leads_by_phone(partner_id, phone,
                                                          include_lost=True).
                           ids)
            if 'name' in fields:
                result['name'] = 'merge' if len(tomerge) >= 2 else 'convert'
            if 'opportunity_ids' in fields and len(tomerge) >= 2:
                result['opportunity_ids'] = list(tomerge)
        return result
