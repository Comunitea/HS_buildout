import logging
from odoo import api, fields, models
_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):

    _inherit = 'project.task'

    def write(self, vals):
        res = super().write(vals)
        if 'stage_id' in vals and self.stage_id.survey_id:

            try:
                if self.stage_id.survey_receiver == "manager":
                    partner_id = self.project_id.responsible_id.partner_id
                else:
                    partner_id = self.project_id.user_id.partner_id
                template = self.env.ref('survey.email_template_survey', raise_if_not_found=False)
                message = self.env['survey.mail.compose.message'].create({
                    'survey_id': self.stage_id.survey_id.id,
                    'public': 'email_private',
                    'partner_ids': [(4, partner_id.id)],
                    'template_id': template.id,
                    'model': self.stage_id.survey_id._name,
                    'res_id': self.stage_id.survey_id.id,
                })
                message.onchange_template_id_wrapper()
                message.send_mail_action()
            except Exception as e:
                _logger.error("survey mail error: {}".format(e))

        if 'stage_id' in vals and self.stage_id.extra_survey_id:
            try:
                if self.stage_id.extra_survey_receiver == "manager":
                    partner_id = self.project_id.responsible_id.partner_id
                else:
                    partner_id = self.project_id.user_id.partner_id
                template = self.env.ref('survey.email_template_survey', raise_if_not_found=False)
                message = self.env['survey.mail.compose.message'].create({
                    'survey_id': self.stage_id.extra_survey_id.id,
                    'public': 'email_private',
                    'partner_ids': [(4, partner_id.id)],
                    'template_id': template.id,
                    'model': self.stage_id.extra_survey_id._name,
                    'res_id': self.stage_id.extra_survey_id.id,
                })
                message.onchange_template_id_wrapper()
                message.send_mail_action()
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
