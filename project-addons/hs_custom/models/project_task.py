from odoo import api, fields, models
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

    @api.depends('stock_move_ids')
    def _compute_can_add_materials(self):
        for record in self:
            if record.stock_move_ids:
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

    # @api.constrains('planned_hours')
    # def _check_planned_hours(self):
    #     for record in self:
    #         if record.planned_hours <=0:
    #             raise ValidationError("Planned hours must be greater than 0")

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        for record in self:
            if record.stage_id and record.stage_id.required_planned_hours and record.planned_hours<=0:
                raise ValidationError("Planned hours must be greater than 0")
            elif record.stage_id and record.stage_id.on_route and (not record.timesheet_ids):
                raise ValidationError("You must add timesheet lines to this task")
            else:
                super()._onchange_stage_id()

    # _sql_constraints = [
    #     ('planned_hours_not_zero',
    #      'CHECK (planned_hours > 0)',
    #      'Planned hours must be greater than 0'),
    # ]

    # @api.model
    # def create(self, vals):
    #     if 'planned_hours' not in vals.keys():
    #         raise ValidationError("Planned hours must be greater than 0")
    #     return super(ProjectTask, self).create(vals)

    @api.multi
    def write(self, values):
        res = super(ProjectTask, self).write(values)
        for record in self:
            if record.planned_hours<=0 and record.stage_id and record.stage_id.required_planned_hours:
                raise ValidationError("Planned hours must be greater than 0")
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

        # task = self[0].task_id
        # pick_type = task.picking_type_id or self.env.ref(
        #     'project_task_material_stock.project_task_material_picking_type')
        # picking_id = task.picking_id or self.env['stock.picking'].create({
        #     'origin': "{}/{}".format(task.project_id.name, task.name),
        #     'partner_id': task.partner_id.id,
        #     'picking_type_id': pick_type.id,
        #     'location_id': pick_type.default_location_src_id.id,
        #     'location_dest_id': pick_type.default_location_dest_id.id,
        # })
        # for line in self:
        #     if not line.stock_move_id:
        #         move_vals = line._prepare_stock_move()
        #         move_vals.update({'picking_id': picking_id.id or False})
        #         move_id = self.env['stock.move'].create(move_vals)
        #         line.stock_move_id = move_id.id
