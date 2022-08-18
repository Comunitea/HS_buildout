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
