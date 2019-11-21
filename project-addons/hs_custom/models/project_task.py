from odoo import fields, models


class ProjectTask(models.Model):

    _inherit = "project.task"

    x_pago_fin = fields.Text("Instrucciones para el pago fin de obra")
