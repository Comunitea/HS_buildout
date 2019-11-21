from odoo import api, models


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.multi
    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, body='', subject=None,
                     message_type='notification', subtype=None,
                     parent_id=False, attachments=None,
                     notif_layout=False, add_sign=True,
                     model_description=False,
                     mail_auto_delete=True, **kwargs):
        autofollow = False

        if self.env.context.get('mail_post_autofollow'):
            autofollow = True
        ctx = dict(self.env.context)
        if autofollow:
            del ctx['mail_post_autofollow']
        return super(MailThread, self.with_context(ctx)).\
            message_post(body=body, subject=subject, message_type=message_type,
                         subtype=subtype, parent_id=parent_id,
                         attachments=attachments, notif_layout=notif_layout,
                         add_sign=add_sign,
                         model_description=model_description,
                         mail_auto_delete=mail_auto_delete, **kwargs)
