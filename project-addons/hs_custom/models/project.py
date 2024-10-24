from odoo import api, fields, models, _

class ProjectProject(models.Model):
    _name = "project.project"
    _inherit = ["project.project", 'mail.activity.mixin']

    @api.depends('x_subtotal', 'x_iva_percentage')
    def _compute_total(self):
        for project in self:
            project.total = project.x_subtotal * (1 + project.x_iva_percentage / 100)

    x_iva_percentage= fields.Float("IVA Percentage", digits=(16, 2))
    x_acc_number = fields.Char("Account Number")
    # x_iva = fields.Boolean("IVA reducido")
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
    x_subtotalneto = fields.Float("Subtotal Neto", digits=(16, 2))
    x_subtotalneto_subcontrata = fields.Float("Subtotal Neto Subcontrata", digits=(16, 2))
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
    responsible_id = fields.Many2one("res.users", "Responsable de proyecto")

    contract_signature = fields.Binary(
        string='Contract acceptance', attachment=True,copy=False
    )
    total = fields.Float("Total", digits=(16, 2), compute="_compute_total")
    analytic_parent_id = fields.Many2one('account.analytic.account',
                                         'Account Analytic parent')

    validated = fields.Boolean("Validated", default=False, copy=False)

    @api.multi
    def write(self, values):
        res = super(ProjectProject, self).write(values)
        if values.get('name') or values.get('analytic_parent_id'):
            for project in self:
                _data={}
                if project.analytic_account_id:
                    _data['name'] = project.name
                    if project.analytic_parent_id:
                        _data['parent_id'] = project.analytic_parent_id.id
                    project.analytic_account_id.write(_data)
        self._track_signature(values, 'contract_signature')
        return res

    def toggle_validate(self):
        for project in self:
            project.validated = not project.validated

    @api.model
    def create(self, values):
        project = super(ProjectProject, self).create(values)
        if project.contract_signature:
            values = {'contract_signature': project.contract_signature}
            project._track_signature(values, 'contract_signature')
        if project.analytic_account_id and project.analytic_parent_id:
            project.analytic_account_id.write({'parent_id': project.analytic_parent_id.id})
        return project

    def action_show_contract_signatures(self):
        return {'type': 'ir.actions.act_window',
                'name': ('Contract Signatures'),
                'res_model': 'contract.signature.wizard',
                'target': 'new',
                'view_id': self.env.ref('hs_custom.view_contract_signature_wzd').id,
                'view_mode': 'form',
                }

    @api.multi
    def action_contract_send(self):
        self.ensure_one()
        template = self.env.ref(
            'hs_custom.email_project_template',
            False,
        )
        compose_form = self.env.ref('mail.email_compose_message_wizard_form',
                                    False)
        ctx = dict(
            default_model='project.project',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            )
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }
