from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    privacy_visibility = fields.Selection(default="employees")
