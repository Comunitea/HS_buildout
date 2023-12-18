from odoo import fields, models

class ResCompany(models.Model):

    _inherit  = 'res.company'

    report_footer_image = fields.Binary(string='Report Footer Image', help='This field holds the image used in the report footer.')
