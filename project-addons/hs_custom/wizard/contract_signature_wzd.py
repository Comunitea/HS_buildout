from odoo import api, fields, models, _

class ContractSignatureWizard(models.TransientModel):
    _name='contract.signature.wizard'


    contract_signature = fields.Binary(
        string='Contract acceptance',
    )
    contract_id = fields.Many2one(comodel_name='project.project', string='Contract')

    @api.model
    def default_get(self, fields):
        res = super(ContractSignatureWizard, self).default_get(fields)
        contract = self.env['project.project'].browse(self._context.get('active_id'))
        res.update({
            'contract_id': contract.id,
            'contract_signature': contract.contract_signature,
        })
        return res

    def action_update_contract_signature(self):
        if self.contract_id.contract_signature != self.contract_signature:
            self.contract_id.write({
                'contract_signature': self.contract_signature,
                'start_date': fields.Date.today(),
            })
        return True
