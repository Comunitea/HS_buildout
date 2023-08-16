from odoo import models, fields, api, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _compute_task_count(self):
        for picking in self:
            material = picking.env['project.task.material'].search(['|',
                                                                    '|',
                                                                    ('stock_move_id','in',picking.move_line_ids.ids),
                                                                    ('stock_move_id','in',picking.move_ids_without_package.ids),
                                                                    ('stock_move_id','in',picking.move_lines.ids)])
            if material:
                tasks = material.mapped('task_id')
                picking.task_count = len(tasks)
            else:
                 picking.task_count = 0

    task_count = fields.Integer(compute='_compute_task_count', string='Task Count')

    def action_view_tasks(self):
        self.ensure_one()
        list_view_id = self.env.ref('project.view_task_tree2').id
        form_view_id = self.env.ref('project.view_task_form2').id
        action = {'type': 'ir.actions.act_window_close'}
        material = self.env['project.task.material'].search(['|',
                                                             '|',
                                                            ('stock_move_id','in',self.move_line_ids.ids),
                                                            ('stock_move_id','in',self.move_ids_without_package.ids),
                                                            ('stock_move_id','in',self.move_lines.ids)])
        if material:
            tasks = material.mapped('task_id')
            if len(tasks)> 0:
                action = self.env["ir.actions.act_window"].for_xml_id("project","action_view_task")
                action['context'] = {}  # erase default context to avoid default filter
                if len(tasks)> 1:  # cross project kanban task
                    action['views'] = [[False, 'kanban'], [list_view_id, 'tree'], [form_view_id, 'form'], [False, 'graph'], [False, 'calendar'], [False, 'pivot']]
                    action['domain'] = [('id','in',tasks.ids)]
                elif len(tasks):  # single task -> form view
                    action['views'] = [(form_view_id, 'form')]
                    action['res_id'] = tasks.id
        return action


class StockMove(models.Model):

    _inherit = 'stock.move'

    from_task = fields.Boolean('From Task', default=False)

    def unlink(self):
        if any(move.from_task for move in self):
            raise UserError(_('You cannot delete consumptions from a task.'))
        return super(StockMove, self).unlink()

