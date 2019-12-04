# -*- coding: utf-8 -*-
from odoo import api, models


class ProjectProject(models.Model):
    _name = "project.project"
    _inherit = ['project.project', 'utm.mixin']

    @api.onchange('partner_id')
    def onchange_partner_id_utm_data(self):
        if self.partner_id:
            self.campaign_id = self.partner_id.campaign_id.id
            self.source_id = self.partner_id.source_id.id
            self.medium_id = self.partner_id.medium_id.id
