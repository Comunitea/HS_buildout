from odoo import api, fields, models, _

class ContractSignatureWizard(models.TransientModel):
    _name='contract.signature.wizard'
    _description = 'Contract Signature Wizard'

    contract_signature = fields.Binary(
        string='Contract acceptance',
    )
    contract_id = fields.Many2one(comodel_name='project.project', string='Contract')

    name = fields.Char('Name')
    x_trabajos = fields.Text('Trabajos a realizar')
    x_condiciones_pagos = fields.Text('Condiciones de Pago')
    x_subtotal = fields.Float('Subtotal')
    x_vendedor = fields.Char('Vendedor')

    @api.model
    def default_get(self, fields):
        res = super(ContractSignatureWizard, self).default_get(fields)
        contract = self.env['project.project'].browse(self._context.get('active_id'))
        res.update({
            'contract_id': contract.id,
            'contract_signature': contract.contract_signature,
            'x_trabajos': contract.x_trabajos,
            'x_condiciones_pagos': contract.x_condiciones_pagos,
            'x_subtotal': contract.x_subtotal,
            'x_vendedor': contract.x_vendedor,
        })
        return res

    def action_update_contract_signature(self):
        if self.contract_signature and self.contract_id.contract_signature != self.contract_signature:
            self.contract_id.write({
                'contract_signature': self.contract_signature,
                'start_date': fields.Date.today(),
            })
            return self.sudo().contract_id.action_contract_send()
        return True
