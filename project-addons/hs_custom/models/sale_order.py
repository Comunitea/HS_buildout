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


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    @api.multi
    def _timesheet_create_project(self):
        project = super()._timesheet_create_project()
        if self.order_id.type_id and not project.sale_type_id:
            project.sale_type_id = self.order_id.type_id.id

        return project

    def _timesheet_create_task_prepare_values(self, project):
        vals = super()._timesheet_create_task_prepare_values(project)
        if self.order_id.type_id:
            vals['sale_type_id'] = self.order_id.type_id.id
        return vals


class SaleOrderType(models.Model):

    _inherit = "sale.order.type"

    logo = fields.Binary("Logo", attachment=True)
