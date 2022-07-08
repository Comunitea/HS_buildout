from odoo import api, fields, models

class SurveyUserInput(models.Model):

    _inherit = 'survey.user_input'

    project_task_id = fields.Many2one('project.task', string='Project task')

    def create(self, vals):
        res = super().create(vals)
        ctx = self.env.context.copy()
        if 'task_id' in ctx:
            res.project_task_id = ctx.get('task_id', False)
        return res
