from odoo import api, models, fields, _
from odoo.exceptions import UserError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.multi
    def write(self, vals):
        res = super(ProjectTask, self).write(vals)
        for task in self:
            if not task.closed:
                if not all(x.location_id == task.location_source_id for x in task.stock_move_ids):
                    task._change_location()
                if task.consume_material and task.stock_move_ids and task.stock_state == 'confirmed':
                    task.action_assign()
            else:
                if task.consume_material and task.stock_move_ids and task.stock_state == 'confirmed':
                    task.action_assign()
                    if task.stock_state == 'assigned':
                        task.action_done()
                    else:
                         raise UserError(_('You cannot validate a transfer if no quantites are reserved nor done.'))
                elif task.consume_material and task.stock_move_ids and task.stock_state == 'assigned':
                    task.action_done()
        return res

    def _change_location(self):
        for record in self:
            if record.stock_move_ids and record.consume_material and not record.closed:
                location = record.location_source_id.id or record.project_id.location_source_id.id or self.env.ref('stock.stock_location_stock').id
                for move in record.stock_move_ids:
                    if move.state not in ('done', 'cancelled'):
                        if move.state == 'assigned':
                            move._do_unreserve()
                        if move.state in ('waiting', 'confirmed', 'assigned'):
                            move.write({'location_id': location})
                # Descomentar en caso de querer cambiar también la localización del albarán
                # if record.picking_id:
                #     record.picking_id.write({'location_id': location})
