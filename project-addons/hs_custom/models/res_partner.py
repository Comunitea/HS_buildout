from odoo import fields, models, api


class ResPartner(models.Model):

    _inherit = "res.partner"

    x_tenant_name = fields.Char("Nombre del inquilino")
    project_ids = fields.One2many('project.project', 'partner_id',
                                  string='Proyectos')
    project_count = fields.Integer(compute='_compute_project_count',
                                   string='# Proyectos')

    def _compute_project_count(self):
        fetch_data = self.env['project.project'].\
            read_group([('partner_id', 'in', self.ids)], ['partner_id'],
                       ['partner_id'])
        result = dict((data['partner_id'][0],
                       data['partner_id_count']) for data in fetch_data)
        for partner in self:
            partner.project_count = result.get(partner.id, 0)


class ResUsers(models.Model):

    _inherit = "res.users"

    sequence = fields.Integer(default=10)
    location_source_id = fields.Many2one(
        comodel_name='stock.location',
        string='Ubicación de consumo',
        help="Location by default for user's task",
    )
    assignment_cycle = fields.Integer('Assignment Cycle', default=1)


class ResUsersList(models.Model):

    _name = "res.users.list"

    def _get_order_type(self):
        return self.env['sale.order.type'].search([], limit=1)

    name = fields.Char("Name")
    state_id = fields.Many2one(comodel_name="res.country.state",
                               string="State")
    user_ids = fields.Many2many(comodel_name="res.users",
                                string="User")
    user_id = fields.Many2one(comodel_name="res.users",
                              string="Last assigned user", readonly=True)
    sale_type_id = fields.Many2one(
        comodel_name='sale.order.type',
        string='Sale Type',
        default=_get_order_type,
        required=True
    )
    assignment_cycle = fields.Integer('Assignment Cycle', readonly=True)

    # def rotate_users(self):
    #     self.ensure_one()

    #     if self.user_ids:
    #         current_user = self.user_id
    #         if current_user:
    #             current_index = self.user_ids.ids.index(current_user.id)
    #             next_index = (current_index + 1) % len(self.user_ids)
    #             next_user = self.user_ids[next_index]
    #             self.last_assigned_user = next_user
    #             self.user_id = next_user
    #         else:
    #             self.user_id = self.user_ids[0]
