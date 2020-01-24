from odoo import api, fields, models


class ProjectProject(models.Model):

    _inherit = "project.project"

    x_iva = fields.Boolean("IVA reducido")
    x_iva_doc = fields.Boolean("Documento de IVA")
    x_info = fields.Boolean("Hoja de información")
    x_plano = fields.Boolean("Plano disponible")
    x_pago_fianza = fields.Boolean("Fianza pagada")
    x_original = fields.Boolean("Contrato original")
    x_street = fields.Char("Calle")
    x_street2 = fields.Char("Calle 2")
    x_city = fields.Char("Ciudad")
    x_zip = fields.Char("C.P.")
    x_state_id = fields.Many2one("res.country.state", "Provincia")
    x_country_id = fields.Many2one("res.country", "País", required=True)
    x_trabajos = fields.Text("Trabajos a realizar", required=True)
    x_condiciones_pagos = fields.Text("Condiciones de Pago", required=True)
    x_subtotal = fields.Float("Subtotal", digits=(16, 2), required=True)
    x_subtotalneto = fields.Float("Subtotal Neto", digits=(16, 2),
                                  required=True)
    x_vendedor = fields.Char("Vendedor", readonly=True)
    x_nif = fields.Char("NIF", readonly=True)
    x_estado = fields.Char("Estado", readonly=True)

    type_id = fields.Many2one('account.analytic.group',
                              "Categoría", required=True)
    start_date = fields.Date("Fecha de firma")
    end_date = fields.Date("Fin de obra")
    sale_type_id = fields.Many2one("sale.order.type", "División")

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            self.x_street = self.partner_id.street
            self.x_street2 = self.partner_id.street2
            self.x_city = self.partner_id.city
            self.x_zip = self.partner_id.zip
            self.x_state_id = self.partner_id.state_id.id
            self.x_country_id = self.partner_id.country_id.id
