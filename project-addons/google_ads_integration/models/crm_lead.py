from odoo import _, api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    gclid = fields.Char(string="GCLID", required=False, readonly=True)


class CrmStage(models.Model):
    _inherit = "crm.stage"

    conversion_name = fields.Selection(
        [
            ("invalid", "Invalid Lead"),
            ("valid", "Valid Lead"),
            ("qualified", "Qualified Lead"),
            ("sale", "Sale"),
        ],
        string="Conversion Name",
    )