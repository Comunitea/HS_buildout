from odoo import fields, models


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

    location_source_id = fields.Many2one(
        comodel_name='stock.location',
        string='Ubicación de consumo',
        help="Location by default for user's task",
    )
