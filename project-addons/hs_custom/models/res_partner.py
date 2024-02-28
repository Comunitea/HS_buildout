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
    zone_ids = fields.Many2many(comodel_name="res.users.zone", string="Zones")


class UsersZone(models.Model):

    _name="res.users.zone"
    _description = "Res Users Zone"

    name = fields.Char("Name")
    user_list_ids = fields.Many2many(comodel_name="res.users.list",string="User List")
    user_ids = fields.Many2many(comodel_name="res.users",string="Managers",
                                domain = lambda self: [('groups_id','in',[self.env.ref('hs_custom.group_sale_salesman_zone_leads').id,
                                                                          self.env.ref('sales_team.group_sale_salesman_all_leads').id ]
                                                        )])


class ResUsersList(models.Model):

    _name = "res.users.list"
    _description = "Res Users List"

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

    zip_ids = fields.Many2many(comodel_name="res.city.zip", string="Zip Codes",
                               domain="[('id', 'in', allowed_zip_ids)]",
                               default=lambda self: self.allowed_zip_ids.ids)

    allowed_zip_ids = fields.Many2many(comodel_name="res.city.zip",
                                       string="Allowed Zip Codes",
                                       compute="_compute_allowed_zip_ids")

    @api.depends('state_id', 'state_id.city_ids')
    def _compute_allowed_zip_ids(self):
        for record in self:
            if record.state_id and record.state_id.city_ids:
                record.allowed_zip_ids = record.state_id.city_ids.mapped('zip_ids')
            else:
                record.allowed_zip_ids = False

    @api.onchange('state_id')
    def _onchange_state_id(self):
        for record in self:
            record.zip_ids = record.allowed_zip_ids
