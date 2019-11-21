from odoo import fields, models


class CrmLead(models.Model):

    _inherit = "crm.lead"

    x_tenant_name = fields.Char("Nombre del inquilino")
    fax = fields.Char("Teléfono inquilino")
    x_date_received = fields.Datetime("Cupón recibido")
    x_estado = fields.Char("Estado")
    x_vendedor = fields.Char("Vendedor")
