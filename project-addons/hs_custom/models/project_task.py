from odoo import api, fields, models


class ProjectTask(models.Model):

    _inherit = "project.task"

    x_pago_fin = fields.Text("Instrucciones para el pago fin de obra")

    @api.onchange('user_id')
    def _onchange_user(self):
        super()._onchange_user()
        if self.user_id and self.user_id.location_source_id:
            self.location_source_id = self.user_id.location_source_id.id
