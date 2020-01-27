# Author: Omar Castiñeira Saavedra
# Copyright 2020 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, exceptions


class WizardAttachPictures(models.TransientModel):
    _name = "wizard.attach.pictures"

    image_ids = fields.Many2many('ir.attachment', string="Pictures",
                                 required=True)

    @api.multi
    def action_save(self):
        if self.env.context.get('active_id'):
            task = self.env['project.task'].\
                browse(self.env.context['active_id'])
            for wzd in self:
                self.image_ids.write({'res_model': 'project.task',
                                      'res_id': task.id})
        else:
            raise exceptions.UserError("No se puede localizar la tarea a la "
                                       "que adjunar las fotografías")
