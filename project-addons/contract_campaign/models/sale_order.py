from odoo import api, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        new_vals = {}
        if self.campaign_id:
            new_vals['campaign_id'] = self.campaign_id.id
        if self.source_id:
            new_vals['source_id'] = self.source_id.id
        if self.medium_id:
            new_vals['medium_id'] = self.medium_id.id
        if new_vals:
            invoice_vals.update(new_vals)
        return invoice_vals


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def _timesheet_create_project(self):
        project = super()._timesheet_create_project()
        new_vals = {}
        if self.order_id.campaign_id:
            new_vals['campaign_id'] = self.order_id.campaign_id.id
        if self.order_id.source_id:
            new_vals['source_id'] = self.order_id.source_id.id
        if self.order_id.medium_id:
            new_vals['medium_id'] = self.order_id.medium_id.id
        if new_vals:
            project.write(new_vals)

        return project
