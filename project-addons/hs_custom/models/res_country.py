from odoo import fields, models


class ResCountryState(models.Model):

    _inherit = "res.country.state"

    user_list_ids = fields.One2many(comodel_name="res.users.list",
                                    inverse_name="state_id",
                                    string="Users List")
