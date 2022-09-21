from odoo import api, fields, models

class SurveyUserInput(models.Model):

    _inherit = 'survey.user_input'

    project_task_id = fields.Many2one('project.task', string='Project task')
    tag_ids = fields.Many2many('project.tags', related="project_task_id.tag_ids", string="Tags")
    worker_id = fields.Many2one("res.users", "Technician", related="project_task_id.worker_id", store=True)
    team_tag = fields.Char(
        string='Team tag',
        compute='_compute_team_tag', store=True)
    survey_last_update = fields.Datetime('Survey Last Date', compute='_compute_survey_last_update', store=True)

    def create(self, vals):
        res = super().create(vals)
        ctx = self.env.context.copy()
        if 'task_id' in ctx:
            res.project_task_id = ctx.get('task_id', False)
        return res

    @api.depends('tag_ids')
    def _compute_team_tag(self):
        for user_input in self:
            team_tag = ""
            for tag in user_input.tag_ids:
                team_tag += " {}".format(tag.name)
            user_input.team_tag = team_tag
    
    @api.depends('user_input_line_ids')
    def _compute_survey_last_update(self):
        for user_input in self:
            if user_input.user_input_line_ids:
                user_input.survey_last_update = max(user_input.user_input_line_ids.mapped('write_date'))
    
    @api.model
    def read_group(
        self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True
    ):
        """Read group customization in order to display the average quizz_score of the group.
        """
        res = read_group_res = super().read_group(
            domain, fields, groupby, offset=offset, limit=limit, orderby=orderby
        )
        if groupby and groupby[0] == "team_tag":
            if 'quizz_score' in fields:
                for user_input in res:
                    if '__domain' in user_input:
                        user_inputs = self.search(user_input['__domain'])
                        total_quizz_score = 0.0
                        total_value = 0.0
                        for record in user_inputs:
                            total_quizz_score += record.quizz_score
                            questions = record.user_input_line_ids.mapped('question_id')
                            for question in questions:
                                if question.labels_ids.mapped('quizz_mark'):
                                    total_value += max(question.labels_ids.mapped('quizz_mark'))
                        if total_value != 0.0:
                            user_input['quizz_score'] = ((total_quizz_score/total_value)*100)
                        else:
                            user_input['quizz_score'] = 0.0
        return res
