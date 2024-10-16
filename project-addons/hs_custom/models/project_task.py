from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ProjectTask(models.Model):

    _inherit = "project.task"

    @api.depends('timesheet_ids','timesheet_ids.employee_id','timesheet_ids.employee_id.timesheet_cost','stock_move_ids','stock_move_ids.product_id','stock_move_ids.product_id.standard_price','stock_move_ids.product_uom_qty')
    def _compute_task_cost(self):
        for record in self:
            cost = 0.0
            for line in record.timesheet_ids:
                cost += line.employee_id.timesheet_cost * line.unit_amount
            for line in record.stock_move_ids.filtered(lambda x: x.state == 'done'):
                cost += line.product_id.standard_price * line.quantity_done
            record.task_cost = cost

    @api.depends('stock_state')
    def _compute_can_add_materials(self):
        for record in self:
            if record.stock_state == 'done':
                record.can_add_materials = False
            else:
                record.can_add_materials = True

    x_pago_fin = fields.Text("Instrucciones para el pago fin de obra")
    sale_type_id = fields.Many2one("sale.order.type", "División",
                                   required=True)
    incidence = fields.Boolean("Incidencia")

    task_cost = fields.Float('Task Cost',default=0.0, compute='_compute_task_cost')
    can_add_materials = fields.Boolean('Add Materials', default=True, compute='_compute_can_add_materials')
    accomodation = fields.Text(string='Accomodation')
    accomodation_url = fields.Char(string='Accomodation URL')

    @api.onchange('user_id')
    def _onchange_user(self):
        # super()._onchange_user()
        if self.user_id and self.user_id.location_source_id:
            self.location_source_id = self.user_id.location_source_id.id

    @api.onchange('project_id')
    def _onchange_project(self):
        res = super()._onchange_project()
        if self.project_id and self.project_id.sale_type_id:
            self.sale_type_id = self.project_id.sale_type_id.id
        if self.project_id and self.project_id.partner_id:
            self.partner_id = self.project_id.partner_id.id
        return res


    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        for record in self:
            if record.stage_id and record.stage_id.required_planned_hours and record.planned_hours<=0:
                raise ValidationError(_("Planned hours must be greater than 0"))
            if record.stage_id and record.stage_id.on_route:
                if not (record.location_source_id and record.location_dest_id):
                    raise ValidationError(_('You must set a source and destination location'))
                if not record.timesheet_ids:
                    raise ValidationError(_("You must add timesheet lines to this task"))
            super()._onchange_stage_id()


    @api.multi
    def write(self, values):
        res = super(ProjectTask, self).write(values)
        for record in self:
            if record.planned_hours<=0 and record.stage_id and record.stage_id.required_planned_hours:
                raise ValidationError(_("Planned hours must be greater than 0"))
        return res


class ProjectTaskType(models.Model):

    _inherit = "project.task.type"

    on_route = fields.Boolean('On route', default=False)
    required_planned_hours = fields.Boolean('Required planned hours', default=False)

class ProjectTaskMaterial(models.Model):

    _inherit = "project.task.material"

    @api.multi
    def create_stock_move(self):
        res = super(ProjectTaskMaterial, self).create_stock_move()
        task = self[0].task_id
        picking_id = task.picking_id
        if picking_id:
            for stock_move in picking_id.move_lines:
                stock_move.write({'from_task': True})
        return res

