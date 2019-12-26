from odoo import fields, models


class ResPartner(models.Model):

    _inherit = "res.partner"

    x_tenant_name = fields.Char("Nombre del inquilino")


class ResUsers(models.Model):

    _inherit = "res.users"

    location_source_id = fields.Many2one(
        comodel_name='stock.location',
        string='Ubicación de consumo',
        help="Location by default for user's task",
    )
