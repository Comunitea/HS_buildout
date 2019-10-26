# -*- coding: utf-8 -*-
from odoo import models, fields


class ProjectProject(models.Model):
    _inherit = 'project.project'

    def _get_campaign_id(self):
        lead_pool = self.env['crm.lead']
        for project in self:
            lead_ids= lead_pool.search([('partner_id', '=',
                                         project.partner_id.id),
                                        ('campaign_id', '!=', False)], limit=1)
            if lead_ids:
                project.campaign_id = lead_ids[0].campaign_id.id

    campaign_id = fields.Many2one("utm.campaign", compute="_get_campaign_id",
                                  string="Campaign", store=True)
