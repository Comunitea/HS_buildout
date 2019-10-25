# -*- coding: utf-8 -*-
from openerp.osv import orm, fields


class project_project(orm.Model):
    _inherit = 'project.project'

    def _get_campaign_id(self, cr, uid, ids, name, arg, context):
        lead_pool = self.pool.get('crm.lead')
        res ={}
        for project in self.browse (cr, uid, ids):
            lead_ids= lead_pool.search(cr, uid, [('partner_id', '=', project.partner_id.id)])
            if lead_ids:
                res[project.id] = lead_pool.browse(cr, uid, lead_ids)[0].campaign_id.id or False
            else:
                res[project.id] = False
        return res

    _columns = {
        'campaign_id': fields.function(_get_campaign_id, method=True, type='many2one', obj="crm.tracking.campaign",
                                       string="Campaign", store=True),
    }
