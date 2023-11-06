from odoo import fields , models


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'
    report_footer_image = fields.Binary(string='Report Footer Image', related="company_id.report_footer_image",help='This field holds the image used in the report footer.')
