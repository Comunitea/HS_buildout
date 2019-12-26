from odoo import fields, models, api


class SaleOrder(models.Model):

    _inherit = "sale.order"

    x_discount_str = fields.Char("Info descuento")

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        if self.analytic_account_id:
            project = self.env['project.project'].\
                search([('analytic_account_id', '=',
                         self.analytic_account_id.id)], limit=1)
            invoice_vals['x_project_id'] = project and project.id or False
        return invoice_vals


class SaleOrderType(models.Model):

    _inherit = "sale.order.type"

    logo = fields.Binary("Logo", attachment=True)
