from odoo import fields, models


class ResPartner(models.Model):

    _inherit = "res.partner"

    x_tenant_name = fields.Char("Nombre del inquilino")
