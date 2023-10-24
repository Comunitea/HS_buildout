from odoo import api, fields, models

class ProjectProject(models.Model):
    _name = "project.project"
    _inherit = ["project.project", 'mail.activity.mixin']

    x_iva_percentage= fields.Float("IVA Percentage", digits=(16, 2))
    x_acc_number = fields.Char("Account Number")
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
    user_id = fields.Many2one(default=None)


    type_id = fields.Many2one('account.analytic.group',
                              "Categoría", required=True)
    start_date = fields.Date("Fecha de firma")
    end_date = fields.Date("Fin de obra")
    sale_type_id = fields.Many2one("sale.order.type", "División",
                                   required=True)
    responsible_id = fields.Many2one("res.users", "Responsable de proyecto",
                                     required=True)

    contract_signature = fields.Binary(
        string='Contract acceptance', attachment=True
    )


    @api.multi
    def write(self, values):
        res = super(ProjectProject, self).write(values)
        if values.get('name'):
            for project in self:
                if project.analytic_account_id and project.allow_timesheets:
                    project.analytic_account_id.write({'name': project.name})
        self._track_signature(values, 'contract_signature')
        self._track_signature(values, 'worksheet_signature')
        return res

    @api.model
    def create(self, values):
        project = super(ProjectProject, self).create(values)
        if project.contract_signature:
            values = {'contract_signature': project.contract_signature}
            project._track_signature(values, 'contract_signature')
        if project.worksheet_signature:
            values = {'worksheet_signature': project.worksheet_signature}
            project._track_signature(values, 'worksheet_signature')
        return project

    def action_show_contract_signatures(self):
        return {'type': 'ir.actions.act_window',
                'name': ('Contract Signatures'),
                'res_model': 'contract.signature.wizard',
                'target': 'new',
                'view_id': self.env.ref('hs_custom.view_contract_signature_wzd').id,
                'view_mode': 'form',
                }
