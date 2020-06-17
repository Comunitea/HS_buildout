from odoo import fields, models, api


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    x_project_id = fields.Many2one("project.project", "Contrato vinculado")
    x_project_id2 = fields.Many2one("project.project", "Contrato 2")
    x_project_id3 = fields.Many2one("project.project", "Contrato 3")
    x_condiciones_pago = fields.Text("Condiciones de pago")
    x_pagable = fields.Boolean("Comisión pagable")
    x_comision_pagada = fields.Boolean("Comisión pagada")
    x_tasa_comision = fields.Float("% comisión", digits=(5, 2))
    x_tasa_comision_2 = fields.Float("% comisión 2", digits=(5, 2))
    x_tasa_comision_3 = fields.Float("% comisión 3", digits=(5, 2))
    x_comision_finconsum = fields.Float("Comisión", digits=(5, 2))
    comment = fields.Text(readonly=False, states={})


class AccountBankStatement(models.Model):

    _inherit = "account.bank.statement"

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if not res.name:
            SequenceObj = self.env['ir.sequence']
            context = {'ir_sequence_date': res.date}
            res.name = SequenceObj.with_context(**context).\
                next_by_code('account.bank.statement')
        return res
