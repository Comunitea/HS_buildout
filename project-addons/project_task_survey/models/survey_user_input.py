from odoo import api, fields, models

class SurveyUserInput(models.Model):

    _inherit = 'survey.user_input'

    project_task_id = fields.Many2one('project.task', string='Project task')
    tag_ids = fields.Many2many('project.tags', related="project_task_id.tag_ids", string="Tags")
    team_tag = fields.Char(
        string='Team tag',
        compute='_compute_team_tag', store=True)

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
                        for record in user_inputs:
                            total_quizz_score += record.quizz_score
                        user_input['quizz_score'] = total_quizz_score/len(user_inputs)
        return res
