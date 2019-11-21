from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        res = super().action_confirm()
        for order in self.filtered(lambda order: order.partner_id in
                                   order.message_partner_ids):
            order.message_unsubscribe([order.partner_id.id])
        return res

    @api.multi
    def _track_subtype(self, init_values):
        return False
