from odoo import fields, models, api, _
from odoo.addons.phone_validation.tools import phone_validation
from odoo.exceptions import UserError


class CrmLead(models.Model):
    _inherit = "crm.lead"

    def _get_order_type(self):
        return self.env['sale.order.type'].search([], limit=1)

    x_tenant_name = fields.Char("Nombre del inquilino")
    fax = fields.Char("Teléfono inquilino")
    x_date_received = fields.Datetime("Cupón recibido")
    x_estado = fields.Char("Estado")
    x_vendedor = fields.Char("Vendedor")
    creation_date = fields.Datetime('Creation Date', index=True,
                                    default=fields.Datetime.now)
    sale_type_id = fields.Many2one(
        comodel_name='sale.order.type',
        string='Sale Type',
        default=_get_order_type
    )
    managed = fields.Boolean("Automatizada", default=False)

    @api.onchange('zip')
    def _onchange_zip(self):
        for record in self:
            zip_id = record.env['res.city.zip'].search([
                ('name', '=', record.zip)], limit=1)
            if zip_id:
                record.state_id = zip_id.city_id.state_id.id or False

    @api.onchange('state_id', 'sale_type_id')
    def _onchange_state_id(self):
        for record in self:
            users_list = record.get_users_list()
            if users_list:
                record.user_id = record.get_user(users_list[0])
            else:
                record.user_id = False

    @api.multi
    def action_set_lost(self):
        res = super().action_set_lost()
        stage = self.env.ref('crm.stage_lead7')
        self.write({'stage_id': stage.id,
                    'active': True})
        return res

    @api.onchange('fax', 'country_id', 'company_id')
    def _onchange_fax_validation(self):
        for record in self:
            if record.fax:
                record.fax = record.phone_format(record.fax)

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.phone:
            res = res.create_opportunity()
        return res

    def phone_format_custom(self, number, country=None, company=None):
        self.ensure_one()
        country = country or self._phone_get_country()
        if not country:
            return number
        always_international = company.phone_international_format == 'prefix'\
            if company else self._phone_get_always_international()
        return phone_validation.phone_format(
            number,
            country.code if country else None,
            country.phone_code if country else None,
            always_international=always_international
        )

    @api.model
    def _get_duplicated_leads_by_phone(self, phone,
                                       include_lost=False):
        if not phone:
            return self.env['crm.lead']
        domain = [('phone', '=', phone)]
        if not include_lost:
            domain += ['&', ('active', '=', True), ('probability', '<', 100)]
        else:
            domain += ['|', '&', ('type', '=', 'lead'), ('active', '=', True),
                       ('type', '=', 'opportunity')]
        return self.env['crm.lead'].search(domain)

    @api.multi
    def action_merge(self, opportunity_ids):
        self.ensure_one()
        return opportunity_ids.merge_opportunity(self.user_id.id,
                                                 self.team_id.id)

    @api.multi
    def create_opportunity(self):
        self.ensure_one()
        if self.phone and not self.managed:
            try:
                number = self.phone_format_custom(
                    self.phone, company=self.company_id)
            except UserError as e:
                number = e
            if isinstance(number, UserError):
                self.message_post(body=_("Invalid phone number ") + self.phone)
                self.phone = ""
                self.action_set_lost()
                self.managed = True
            else:
                campaign_id = self.campaign_id
                users_list = self.get_users_list()
                tomerge = self._get_duplicated_leads_by_phone(
                    self.phone, include_lost=False)
                if len(tomerge) >= 2:
                    users = tomerge.mapped('user_id').filtered(
                        lambda x: x.active)
                    self = self.action_merge(tomerge)
                    self.campaign_id = campaign_id
                    if users:
                        self.allocate_salesman([users[0].id], self.team_id.id)
                    elif users_list and self.user_id in users_list.user_ids:
                        self.allocate_salesman([self.user_id.id], self.team_id.id)
                elif users_list and self.user_id in users_list.user_ids:
                    self.convert_opportunity(self.partner_id.id,
                                             [self.user_id.id], self.team_id.id)
                    self.managed = True
                    self.message_post(body="Cupón nuevo", subtype='mail.mt_comment')
        elif not self.phone and not self.managed:
            self.managed = True
            self.action_set_lost()

        return self

    @api.multi
    def get_users_list(self):
        self.ensure_one()
        if self.state_id and self.state_id.user_list_ids:
            users_list = self.state_id.user_list_ids.filtered(
                lambda x: x.sale_type_id == self.sale_type_id)
            if users_list:
                return users_list[0]
            else:
                return False
        else:
            return False

    def get_user(self, users_list):
        users_list.ensure_one()
        if users_list.user_ids:
            current_user = users_list.user_id
            if current_user and current_user in users_list.user_ids:
                current_index = users_list.user_ids.sorted('sequence').ids.index(current_user.id)
                next_index = (current_index + 1) % len(users_list.user_ids)
                next_user = users_list.user_ids.sorted('sequence')[next_index]
                return next_user
            else:
                return users_list.user_ids[0]
        else:
            return False

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        if vals.get('state_id') and not vals.get('user_id'):
            for lead in self:
                users_list = lead.get_users_list()
                if users_list:
                    if users_list.user_id != self.user_id:
                        users_list.user_id = self.user_id
        for lead in self:
            if lead.type == 'lead' and lead.phone:
                lead.create_opportunity()
        return res
