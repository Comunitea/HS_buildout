from odoo import fields, models, api


class ResCountryState(models.Model):

    _inherit = "res.country.state"

    user_list_ids = fields.One2many(comodel_name="res.users.list",
                                    inverse_name="state_id",
                                    string="Users List")

    city_ids = fields.One2many(comodel_name="res.city", inverse_name="state_id", string="Cities")

