from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def invoice_validate(self):
        res = super().invoice_validate()
        for invoice in self.filtered(lambda invoice: invoice.partner_id in
                                     invoice.message_partner_ids):
            invoice.message_unsubscribe([invoice.partner_id.id])
        return res
