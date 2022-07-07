from odoo import api, fields, models

class SurveyUserInput(models.Model):

    _inherit = 'survey.user_input'

    project_task_id = fields.Many2one('project.task', string='Project task')

    def create(self, vals):
        res = super().create(vals)
        params = self.env.context.get('params', False)
        if params and params.get('model', False) == 'project.task' and params.get('id', False):
            res.project_task_id = params.get('id', False)
        return res
