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
                    elif task.stock_state == 'confirmed':
                        if all([x.state == 'assigned' or x.quantity_done == x.product_uom_qty for x in task.stock_move_ids.filtered(lambda m: m.state not in ('done', 'cancel'))]):
                            task.action_done()
                        else:
                            raise UserError(_('You cannot validate a transfer if no quantites are reserved nor done. To force the transfer, switch in edit more and encode the done quantities.'))
                    else:
                         raise UserError(_('You cannot validate a transfer if no quantites are reserved nor done. To force the transfer, switch in edit more and encode the done quantities.'))
                elif task.consume_material and task.stock_move_ids and task.stock_state == 'assigned':
                    task.action_done()
        return res

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        for record in self:
            if record.stage_id and record.stage_id.consume_material:
                if not(record.material_ids):
                    raise UserError(_('You must add materials in order to consume them'))
                # elif not (record.location_source_id and record.location_dest_id):
                #     raise UserError(_('You must set a source and destination location in order to consume materials'))


    def _change_location(self):
        for record in self:
            if record.stock_move_ids and record.consume_material and not record.closed:
                location = record.location_source_id.id or record.project_id.location_source_id.id or self.env.ref('stock.stock_location_stock').id
                for move in record.stock_move_ids:
                    if move.state not in ('done', 'cancelled'):
                        if move.state == 'assigned':
                            move._do_unreserve()
                        if move.state in ('draft','waiting', 'confirmed', 'assigned','partially_available'):
                            move.write({'location_id': location})
                # Descomentar en caso de querer cambiar también la localización del albarán
                # if record.picking_id:
                #     record.picking_id.write({'location_id': location})

    @api.multi
    def action_assign(self):
        super(ProjectTask, self).action_assign()
        if self.env.context.get('do_unreserve', False):
            for move in self.mapped('stock_move_ids').filtered(lambda x: x.state == 'confirmed'):
                quants = self.env['stock.quant'].search([('product_id', '=', move.product_id.id), ('location_id', '=', move.location_id.id),('quantity', '>', 0)])
                quantity = sum(quants.mapped('quantity'))
                if quantity >= move.product_uom_qty:
                    moves = self.env['stock.move'].search([('product_id','=',move.product_id.id),('location_id','=',move.location_id.id),
                                                            ('state','not in',['done','cancel']),
                                                            ('id','!=',move.id),
                                                            ('picking_id','!=',move.picking_id.id)])
                    same_quantity = moves.filtered(lambda x: x.reserved_availability == move.product_uom_qty)
                    less_quantity = moves.filtered(lambda x: x.reserved_availability < move.product_uom_qty)
                    more_quantity = moves.filtered(lambda x: x.reserved_availability > move.product_uom_qty).sorted(key=lambda x: x.reserved_availability)
                    if same_quantity:
                        same_quantity[0]._do_unreserve()
                    else:
                        if less_quantity and sum(less_quantity.mapped('reserved_availability')) >= move.product_uom_qty:
                            if sum(less_quantity.mapped('reserved_availability')) == move.product_uom_qty:
                                less_quantity._do_unreserve()
                            else:
                                qty = 0
                                for x in less_quantity:
                                    if qty < move.product_uom_qty:
                                        qty += x.reserved_availability
                                        x._do_unreserve()
                                    else:
                                        break
                        elif more_quantity:
                            more_quantity[0]._do_unreserve()
            if self.stock_move_ids.filtered(lambda x: x.state in ['confirmed']):
                self.with_context(do_unreserve=False).action_assign()

class ProjectTaskMaterial(models.Model):

    _inherit = 'project.task.material'

    stock_state = fields.Selection(related='stock_move_id.state', string='State', readonly=True)

    def action_move_cancel(self):
        for record in self:
            if record.stock_move_id:
                record.stock_move_id._action_cancel()
                record.analytic_line_id.unlink()
