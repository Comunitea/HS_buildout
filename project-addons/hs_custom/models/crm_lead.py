from odoo import fields, models, api


class CrmLead(models.Model):

    _inherit = "crm.lead"

    x_tenant_name = fields.Char("Nombre del inquilino")
    fax = fields.Char("Teléfono inquilino")
    x_date_received = fields.Datetime("Cupón recibido")
    x_estado = fields.Char("Estado")
    x_vendedor = fields.Char("Vendedor")
    creation_date = fields.Datetime('Creation Date', index=True,
                                    default=fields.Datetime.now)

    @api.multi
    def action_set_lost(self):
        res = super().action_set_lost()
        stage = self.env.ref('crm.stage_lead7')
        self.write({'stage_id': stage.id,
                    'active': True})
        return res
