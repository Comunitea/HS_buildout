# -*- coding: utf-8 -*-
from odoo import api, models


class ProjectProject(models.Model):
    _name = "project.project"
    _inherit = ['project.project', 'utm.mixin']

    @api.onchange('partner_id')
    def onchange_partner_id_utm_data(self):
        if self.partner_id:
            lead = self.env['crm.lead'].\
                search([('partner_id', '=', self.partner_id.id)], limit=1)
            self.campaign_id = self.partner_id.campaign_id.id or \
                (lead and lead.campaign_id.id or False)
            self.source_id = self.partner_id.source_id.id or \
                (lead and lead.source_id.id or False)
            self.medium_id = self.partner_id.medium_id.id or \
                (lead and lead.medium_id.id or False)
