from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'


    @api.multi
    def _get_next_ref(self, vals=None):
        if (vals and vals.get('customer', False)) or self.customer:
            return super(ResPartner, self)._get_next_ref(vals=vals)
        else:
            return self.env['ir.sequence'].next_by_code('res.partner.supplier')

    @api.model
    def create(self, vals):
        if not (vals.get('customer', False) or vals.get('supplier', False)) and self._needsRef(vals=vals):
            raise ValidationError(_('You must select the type of partner'))
        return super(ResPartner, self).create(vals)
