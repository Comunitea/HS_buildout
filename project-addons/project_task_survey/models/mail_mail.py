import logging
from datetime import datetime, timedelta
from odoo import api, fields, models
_logger = logging.getLogger(__name__)


class MailMail(models.Model):

    _inherit = 'mail.mail'

    def create(self, vals):
        ctx = self.env.context.copy()
        default_scheduled_date = ctx.get("default_scheduled_date", False)
        if default_scheduled_date:
            vals['scheduled_date'] = default_scheduled_date
        res = super().create(vals)        
        return res

    @api.multi
    def send(self, auto_commit=False, raise_exception=False):
        ctx = self.env.context.copy()
        if ctx.get("default_scheduled_date", False):
            return
        return super().send(auto_commit, raise_exception)
