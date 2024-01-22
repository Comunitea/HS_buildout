from odoo import api, fields, models, _


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    correct_completation = fields.Float("Correct Completation %", digits=(16, 2), group_operator="avg")
    execution_time = fields.Float("Execution Time %", digits=(16, 2), group_operator="avg")
    consumed_materials = fields.Float("Consumed Materials %", digits=(16, 2), group_operator="avg")
    photo_report = fields.Float("Photo Report %", digits=(16, 2), group_operator="avg")
    timesheet_signed = fields.Float("Signed Timesheet %", digits=(16, 2), group_operator="avg")
    timesheet_total = fields.Float("Total %", digits=(16, 2), compute="_compute_total",store=True ,group_operator="avg")
    survey_date = fields.Date("Survey Conducted On")

    @api.depends('correct_completation','execution_time','consumed_materials','photo_report','timesheet_signed')
    def _compute_total(self):
        for record in self:
            record.timesheet_total = (record.correct_completation + record.execution_time + record.consumed_materials + record.photo_report + record.timesheet_signed)/5.0
