from odoo import api, fields, models


class ProjectTask(models.Model):

    _inherit = "project.task"

    x_pago_fin = fields.Text("Instrucciones para el pago fin de obra")
    sale_type_id = fields.Many2one("sale.order.type", "División",
                                   required=True)
    incidence = fields.Boolean("Incidencia")

    @api.onchange('user_id')
    def _onchange_user(self):
        super()._onchange_user()
        if self.user_id and self.user_id.location_source_id:
            self.location_source_id = self.user_id.location_source_id.id

    @api.onchange('project_id')
    def _onchange_project(self):
        res = super()._onchange_project()
        if self.project_id and self.project_id.sale_type_id:
            self.sale_type_id = self.project_id.sale_type_id.id
        if self.project_id and self.project_id.partner_id:
            self.partner_id = self.project_id.partner_id.id
        return res
