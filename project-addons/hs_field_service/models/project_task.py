# Author: Omar Castiñeira Saavedra
# Copyright 2020 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, exceptions, _


class ProjectTask(models.Model):

    _inherit = "project.task"

    work_description = fields.Html("Work Description")
    closed = fields.Boolean("Closed", related="stage_id.closed",
                            readonly=True)
    installation = fields.Boolean("Installation")
    warranty = fields.Boolean("Warranty")
    maintenance = fields.Boolean("Maintenance")
    success = fields.Boolean("Successfully")
    cancelled = fields.Boolean("Customer cancellation")
    observations = fields.Html("Observations")
    worker_id = fields.Many2one("res.users", "Technician")
    project_street = fields.Char("Calle", related="project_id.x_street",
                                 readonly=True)
    project_street2 = fields.Char("Calle 2", related="project_id.x_street2",
                                  readonly=True)
    project_zip = fields.Char("C.P-", related="project_id.x_zip",
                              readonly=True)
    project_city = fields.Char("Ciudad", related="project_id.x_city",
                               readonly=True)
    project_state_id = fields.Many2one("res.country.state", "Provincia",
                                       related="project_id.x_state_id",
                                       readonly=True)
    project_country_id = fields.Many2one("res.country", "País",
                                         related="project_id.x_country_id",
                                         readonly=True)

    def action_close_send(self):
        closed_state = self.env['project.task.type'].\
            search([('closed', '=', True)])
        template = self.env.ref(
            'project_task_send_by_mail.email_task_template',
            False,
        )
        if not closed_state:
            raise exceptions.UserError(_("Any stage set as closed stage"))
        if len(closed_state) > 1:
            raise exceptions.UserError(_("Cannot exists more than one stage "
                                         "set as closed."))
        for task in self:
            task.sudo().stage_id = closed_state.id
            template.send_mail(task.id)



class ProjectTaskMaterial(models.Model):

    _inherit = "project.task.material"

    name = fields.Char("Description", compute="_get_rec_name")

    @api.multi
    def _get_rec_name(self):
        for rec in self:
            rec.name = u"{} ({})".format(rec.product_id.display_name,
                                         str(rec.quantity) + " " +
                                         rec.product_id.uom_id.name)

    def _prepare_stock_move(self):
        res = super()._prepare_stock_move()
        res['location_id'] = (
            self.task_id.location_source_id.id or
            self.task_id.user_id.location_source_id.id or
            self.task_id.project_id.location_source_id.id or
            self.env.ref('stock.stock_location_stock').id)
        return res
