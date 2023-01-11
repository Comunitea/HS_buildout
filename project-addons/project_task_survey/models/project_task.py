import logging
from datetime import datetime, timedelta
from odoo import api, fields, models
_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):

    _inherit = 'project.task'

    def send_date_start_survey(self):
        partner_id = self.user_id.partner_id
        template = self.env.ref('survey.email_template_survey', raise_if_not_found=False)
        on_create_survey_id = self.env["ir.config_parameter"].sudo().get_param("project_task_survey.on_create_survey_id")
        survey_id = self.env['survey.survey'].browse(int(on_create_survey_id))

        message = self.env['survey.mail.compose.message'].create({
            'survey_id': survey_id.id,
            'public': 'email_private',
            'partner_ids': [(4, partner_id.id)],
            'template_id': template.id,
            'model': survey_id._name,
            'res_id': survey_id.id,
        })
        ctx = self.env.context.copy()
        ctx['task_id'] = self.id
        ctx['default_scheduled_date'] = self.date_start
        message.onchange_template_id_wrapper()
        message.subject = "{}: {}".format(self.display_name, survey_id.title)
        message.with_context(ctx).send_mail_action()

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if 'date_start' in vals:
            try:
                res.send_date_start_survey()
            except Exception as e:
                _logger.error("survey mail error: {}".format(e))
        return res

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        if 'stage_id' in vals and self.stage_id.survey_id:

            try:
                if self.stage_id.survey_receiver == "manager":
                    partner_id = self.user_id.partner_id
                else:
                    survey_marketing_user = self.env["ir.config_parameter"].sudo().get_param("project_task_survey.survey_marketing_user")
                    partner_id = self.env['res.partner'].browse(int(survey_marketing_user))
                template = self.env.ref('survey.email_template_survey', raise_if_not_found=False)
                message = self.env['survey.mail.compose.message'].create({
                    'survey_id': self.stage_id.survey_id.id,
                    'public': 'email_private',
                    'partner_ids': [(4, partner_id.id)],
                    'template_id': template.id,
                    'model': self.stage_id.survey_id._name,
                    'res_id': self.stage_id.survey_id.id,
                })
                ctx = self.env.context.copy()
                ctx['task_id'] = self.id
                message.onchange_template_id_wrapper()
                message.subject = "{}: {}".format(self.display_name, self.stage_id.survey_id.title)
                message.with_context(ctx).send_mail_action()
            except Exception as e:
                _logger.error("survey mail error: {}".format(e))

        # We only send the extra survey if it's not an incidence.
        if 'stage_id' in vals and self.stage_id.extra_survey_id and not self.incidence:
            try:
                if self.stage_id.extra_survey_receiver == "manager":
                    partner_id = self.user_id.partner_id
                else:
                    survey_marketing_user = self.env["ir.config_parameter"].sudo().get_param("project_task_survey.survey_marketing_user")
                    partner_id = self.env['res.partner'].browse(int(survey_marketing_user))
                template = self.env.ref('survey.email_template_survey', raise_if_not_found=False)
                message = self.env['survey.mail.compose.message'].create({
                    'survey_id': self.stage_id.extra_survey_id.id,
                    'public': 'email_private',
                    'partner_ids': [(4, partner_id.id)],
                    'template_id': template.id,
                    'model': self.stage_id.extra_survey_id._name,
                    'res_id': self.stage_id.extra_survey_id.id,
                })
                ctx = self.env.context.copy()
                ctx['task_id'] = self.id
                # We add a delay of 7 days
                ctx['default_scheduled_date'] = datetime.now() + timedelta(weeks=1)
                message.onchange_template_id_wrapper()
                message.subject = "{}: {}".format(self.display_name, self.stage_id.extra_survey_id.title)
                message.with_context(ctx).send_mail_action()
            except Exception as e:
                _logger.error("survey mail error: {}".format(e))

        if 'date_start' in vals:
            try:
                self.send_date_start_survey()
            except Exception as e:
                _logger.error("survey mail error: {}".format(e))
        return res


class ProjectTaskType(models.Model):

    _inherit = 'project.task.type'

    survey_id = fields.Many2one('survey.survey', string="Survey")
    survey_receiver = fields.Selection([
        ('manager', 'Manager'),
        ('marketing', 'Marketing')
    ], string='Receiver', default="manager")
    extra_survey_id = fields.Many2one('survey.survey', string="Extra survey")
    extra_survey_receiver = fields.Selection([
        ('manager', 'Manager'),
        ('marketing', 'Marketing')
    ], string='Extra survey receiver', default="manager")
