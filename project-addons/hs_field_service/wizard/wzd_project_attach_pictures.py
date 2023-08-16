from odoo import api, models, fields, _


class WizardPorjectAttachPictures(models.TransientModel):
    _name="wizard.project.attach.pictures"

    image_ids = fields.Many2many('ir.attachment', string="Pictures",
                                    required=True)

    @api.multi
    def action_save(self):
        if self.env.context.get('active_id'):
            project = self.env['project.project'].\
                browse(self.env.context['active_id'])
            for wzd in self:
                self.image_ids.write({'res_model': 'project.project',
                                      'res_id': project.id})
        else:
            raise exceptions.UserError("No se puede localizar el proyecto al "
                                       "que adjunar las fotografías")
